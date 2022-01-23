package working

import (
	"bytes"
	"fmt"
	"github.com/imakiri/golang-stepik/testlib"
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

func (t *Test) Test(handler testlib.Handler) bool {
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

func NewTest(validators []testlib.Validator, units []interface{}, timeout time.Duration, args []string) (*Test, error) {
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
	test.args = args

	return test, nil
}
