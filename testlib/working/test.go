package working

import (
	"bytes"
	"fmt"
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

type test struct {
	validators []Validator
	units      []interface{}
	timeout    time.Duration
	delay      time.Duration
	args       []string
	feedback   string
	error      error
}

func (t *test) Args() []string {
	return t.args
}

func (t *test) Timeout() time.Duration {
	return t.timeout
}

func (t *test) Delay() time.Duration {
	return t.delay
}

func (t *test) Feedback() string {
	return t.feedback
}

func (t *test) Error() error {
	return t.error
}

func (t *test) Validate(code string) error {
	var err error
	for i := range t.validators {
		if err = t.validators[i].Validate(code); err != nil {
			return err
		}
	}
	return nil
}

func (t *test) Test(handler io.ReadWriter) bool {
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
			var text []byte
			var b = make([]byte, 1)

			for {
				if bytes.Contains(text, []byte(u.Expected)) {
					t.feedback = ""
					break
				}

				for {
					var _, err = handler.Read(b)
					if err != nil {
						continue
					} else {
						break
					}
				}

				text = append(text, b[0])
			}
		default:
			return false
		}
	}
	return true
}

func NewTest(validators []Validator, units []interface{}, timeout time.Duration, initialDelay time.Duration, args []string) (*test, error) {
	var test = new(test)
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

