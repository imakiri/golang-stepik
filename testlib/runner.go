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
	Test(handler io.ReadWriter) bool
}

type Handler interface {
	io.ReadWriteCloser
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

func (r *runner) Run() (result bool, feedback string, err error) {
	for i := range r.tests {
		var handler, err = NewHandler(r.filename, r.tests[i].Args())
		if err != nil {
			return false, "", err
		}

		var ch = make(chan bool, 1)
		go func() {
			time.Sleep(r.tests[i].Delay())
			ch <- r.tests[i].Test(handler)
		}()

		select {
		case result = <-ch:
		case <-time.After(r.tests[i].Timeout()):
			result = false
		}

		if err = handler.Close(); err != nil {
			return result, feedback, err
		}
		if err = r.tests[i].Error(); err != nil {
			return result, feedback, err
		}

		feedback = r.tests[i].Feedback()
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
	var runner = new(runner)
	runner.tests = tests
	runner.filename = filename
	return runner, nil
}
