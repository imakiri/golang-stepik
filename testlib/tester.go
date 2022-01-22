package testlib

import (
	"bytes"
	"fmt"
	"github.com/golang-collections/go-datastructures/bitarray"
	"io"
	"time"
)

type Validator interface {
	Validate(code string) error
}

type Handler interface {
	io.ReadWriteCloser
	Buffer() (*bytes.Buffer, bitarray.BitArray, uint64)
}

type Test interface {
	Args() []string
	Timeout() time.Duration
	Scanner(handler Handler) bool
	Feedback() string
	Error() error
}

type tester struct {
	tests []Test
}

func (t *tester) Test(filename string) (result bool, feedback string, err error) {
	for i := range t.tests {
		var handler, err = NewHandler(filename, t.tests[i].Args())
		if err != nil {
			return false, "", err
		}

		var ch = make(chan bool, 1)
		go func() {
			ch <- t.tests[i].Scanner(handler)
		}()

		select {
		case result = <-ch:
			break
		case <-time.After(t.tests[i].Timeout()):
			result = false
		}

		if err = handler.Close(); err != nil {
			return result, feedback, err
		}
		if err = t.tests[i].Error(); err != nil {
			return result, feedback, err
		}

		feedback = t.tests[i].Feedback()
		fmt.Println("")
		var f, e = Traceback(handler.Buffer())
		err = e
		fmt.Printf("%s\n\n", f)
	}
	return
}

func NewTester(tests []Test) (*tester, error) {
	var tester = new(tester)
	tester.tests = tests
	return tester, nil
}
