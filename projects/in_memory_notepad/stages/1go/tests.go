package main

import (
	"github.com/imakiri/golang-stepik/testlib"
	"github.com/imakiri/golang-stepik/testlib/working"
	"time"
)

func MustNewTest(units []interface{}) testlib.Test {
	var t, err = working.NewTest(units, 1000*time.Second, []string{})
	if err != nil {
		panic(err)
	}

	return t
}

var feedback_command = "The program should print back only the given command and no more"

func main() {
	var tests = []testlib.Test{
		MustNewTest([]interface{}{
			working.Output{
				Expected: "Enter command and data: ",
				Feedback: "",
			},
			working.Input{Command: "create ethetj"},
			working.Output{
				Expected: "create",
				Feedback: feedback_command,
			},
			working.Output{
				Expected: "Enter command and data: ",
				Feedback: "",
			},
			working.Input{Command: "delete gffgfg"},
			working.Output{
				Expected: "delete",
				Feedback: feedback_command,
			},
		}),
	}

	var runner = testlib.NewRunner(tests)
	runner.Run()
}
