package testlib

import (
	"fmt"
	"io"
	"time"
)

type Validator interface {
	Validate(code string) error
}

type Tester interface {
	Test(handler Handler) bool
}

type Handler interface {
	io.ReadWriteCloser
	Buffers() (trace *buffer, in *buffer, out *buffer, err error)
}

type Test interface {
	Args() []string
	Timeout() time.Duration
	Delay() time.Duration
	Feedback() string
	Error() error
	Validator
	Tester
}

type runner struct {
	tests    []Test
	filename string
}

func (t *runner) Run() (result bool, feedback string, err error) {
	for i := range t.tests {
		var handler, err = NewHandler(t.filename, t.tests[i].Args())
		if err != nil {
			return false, "", err
		}

		var ch = make(chan bool, 1)
		go func() {
			time.Sleep(t.tests[i].Delay())
			ch <- t.tests[i].Test(handler)
		}()

		select {
		case result = <-ch:
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
		var trace, in, out, _ = handler.Buffers()
		fmt.Print("\n---------------------------\n")
		fmt.Println(trace.String())
		fmt.Print("\n---------------------------\n")
		fmt.Println(in.String())
		fmt.Print("\n---------------------------\n")
		fmt.Println(out.String())
		fmt.Print("\n---------------------------\n")
	}
	return
}

func NewRunner(tests []Test, filename string) (*runner, error) {
	var tester = new(runner)
	tester.tests = tests
	tester.filename = filename
	return tester, nil
}
