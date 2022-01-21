package working

import (
	"bufio"
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
	units    []interface{}
	timeout  time.Duration
	args     []string
	feedback string
}

func (t *Test) Args() []string {
	return t.args
}

func (t *Test) Timeout() time.Duration {
	return t.timeout
}

func (t *Test) Scanner(handler testlib.Handler) bool {
	for i := range t.units {
		switch u := t.units[i].(type) {
		case Input:
			var _, err = handler.WriteString(u.Command + "\n")
			if err != nil {
				t.feedback = err.Error()
				return false
			}
		case Output:
			var r = bufio.NewReader(handler)
			t.feedback = u.Feedback
			var line []byte

			for {
				var s, err = r.ReadString(u.Expected[len(u.Expected)-1])
				if err != nil {
					break
				}

				line = append(line, []byte(s)...)
				if bytes.Contains(line, []byte(u.Expected)) {
					break
				}
			}

			t.feedback = ""
		default:
			return false
		}
	}

	_ = handler.Close()
	return true
}

func (t *Test) Feedback() string {
	return t.feedback
}

func NewTest(units []interface{}, timeout time.Duration, args []string) (*Test, error) {
	var test = new(Test)
	for i := range units {
		switch units[i].(type) {
		case Input, Output:
			continue
		default:
			return nil, fmt.Errorf("type %T is not supported", units[i])
		}
	}

	test.units = units
	test.timeout = timeout
	test.args = args

	return test, nil
}
