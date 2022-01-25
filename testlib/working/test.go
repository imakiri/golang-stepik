package working

import (
	"bytes"
	"fmt"
	"github.com/imakiri/golang-stepik/testlib"
	"io"
	"time"
)

type Input struct {
	Command string
}

type Output struct {
	Expected string
	Feedback string
}

//type OneOf struct {
//	outputs []Output
//}

type Test struct {
	validators []testlib.Validator
	units      []interface{}
	timeout    time.Duration
	delay      time.Duration
	args       []string
	feedback   string
	error      error
}

func (t *Test) Args() []string {
	return t.args
}

func (t *Test) Timeout() time.Duration {
	return t.timeout
}

func (t *Test) Delay() time.Duration {
	return t.delay
}

func (t *Test) Feedback() string {
	return t.feedback
}

func (t *Test) Error() error {
	return t.error
}

func (t *Test) Validate(code string) error {
	var err error
	for i := range t.validators {
		if err = t.validators[i].Validate(code); err != nil {
			return err
		}
	}
	return nil
}

func (t *Test) Test(handler io.ReadWriter) bool {
	for i := range t.units {
		switch u := t.units[i].(type) {
		case Input:
			var _, err = handler.Write([]byte(u.Command + "\n"))
			if err != nil {
				t.error = err
				return false
			}
		case Output:
			t.feedback = u.Feedback
			var line []byte
			var b = make([]byte, 1)

			for {
				if bytes.Contains(line, []byte(u.Expected)) {
					break
				}

				var _, err = handler.Read(b)
				if err != nil {
					continue
				}

				line = append(line, b[0])
			}

			t.feedback = ""
		default:
			return false
		}
	}
	return true
}

func NewTest(validators []testlib.Validator, units []interface{}, timeout time.Duration, initialDelay time.Duration, args []string) (*Test, error) {
	var test = new(Test)
	for i := range units {
		switch units[i].(type) {
		case Input, Output:
			continue
		default:
			return nil, fmt.Errorf("type %T is not supported", units[i])
		}
	}

	test.validators = validators
	test.units = units
	test.timeout = timeout
	test.delay = initialDelay
	test.args = args

	return test, nil
}

type handler struct {
	in  io.ReadCloser
	out io.WriteCloser
	err io.WriteCloser
}

func (h *handler) Read(p []byte) (n int, err error) {
	return h.in.Read(p)
}

func (h *handler) Write(p []byte) (n int, err error) {
	return h.out.Write(p)
}

func (h *handler) Close() error {
	h.out.Close()
	h.err.Close()
	return nil
}

func Tester(in io.ReadCloser, out io.WriteCloser, err io.WriteCloser, tests []testlib.Test) {
	var handler = new(handler)
	handler.in = in
	handler.out = out
	handler.err = err
	defer handler.Close()

	for i := range tests {
		var result bool
		var err error

		var ch = make(chan bool, 1)
		go func() {
			time.Sleep(tests[i].Delay())
			ch <- tests[i].Test(handler)
		}()

		select {
		case result = <-ch:
		case <-time.After(tests[i].Timeout()):
			result = false
		}

		if !result {
			fmt.Fprintln(handler.err, "false")
			fmt.Fprintln(handler.err, tests[i].Feedback())
			return
		}

		if err = tests[i].Error(); err != nil {
			io.WriteString(handler.err, "false\n")
			io.WriteString(handler.err, err.Error())
			return
		}
	}

	fmt.Fprintln(handler.err, "true")
}
