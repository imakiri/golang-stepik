package testlib

import (
	"io"
	"time"
)

type Validator interface {
	Validate(code string) error
}

type Handler interface {
	io.Reader
	io.Writer
	io.StringWriter
	io.Closer
}

type Test interface {
	Args() []string
	Timeout() time.Duration
	Scanner(handler Handler) bool
	Feedback() string
}

type tester struct {
	tests []Test
}

func (t *tester) Test() (result bool, feedback string) {
	for i := range t.tests {
		var handler, err = NewHandler(t.tests[i].Args())
		if err != nil {
			return false, err.Error()
		}

		var ch = make(chan bool, 1)
		go func() {
			ch <- t.tests[i].Scanner(handler)
		}()

		select {
		case result = <-ch:
			feedback = t.tests[i].Feedback()
		case <-time.After(t.tests[i].Timeout()):
			result = false
			feedback = t.tests[i].Feedback()
		}
	}
	return
}

func NewTester(tests []Test) (*tester, error) {
	var tester = new(tester)
	tester.tests = tests
	return tester, nil
}
