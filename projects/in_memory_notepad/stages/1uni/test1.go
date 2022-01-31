package main

import (
	"github.com/imakiri/golang-stepik/testlib/working"
	"os"
	"time"
)

func MustNewTest(units []interface{}) working.Test {
	var t, err = working.NewTest(nil, units, time.Second, 10*time.Millisecond, []string{})
	if err != nil {
		panic(err)
	}

	return t
}

var feedback_command = "The program should print back only the given command and no more"

func main() {
	working.Run(os.Stdin, os.Stdout, os.Stderr, MustNewTest([]interface{}{
		working.Output{
			Expected: "",
			Feedback: feedback_command,
		},
		working.Input{Command: "create ethetj"},
		working.Output{
			Expected: "create",
			Feedback: feedback_command,
		},
		working.Input{Command: "delete gffgfg"},
		working.Output{
			Expected: "delete",
			Feedback: feedback_command,
		},
	}))
}
