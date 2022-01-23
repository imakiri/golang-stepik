package main

import (
	"github.com/imakiri/golang-stepik/testlib"
	"github.com/imakiri/golang-stepik/testlib/working"
	"time"
)

func MustNewTest(units []interface{}) testlib.Test {
	var t, err = working.NewTest(nil, units, time.Second, []string{})
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
				Expected: "E",
				Feedback: "",
			},
			working.Input{Command: "create ethetj"},
			working.Output{
				Expected: "create",
				Feedback: feedback_command,
			},
			working.Output{
				Expected: "Enter command and data fdgfdg: ",
				Feedback: "The program should ask user for a command",
			},
			working.Input{Command: "delete gffgfg"},
			working.Output{
				Expected: "delete",
				Feedback: feedback_command,
			},
		}),
	}

	var main = testlib.NewMain(tests)
	main.Execute()
}
