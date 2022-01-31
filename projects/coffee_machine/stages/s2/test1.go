package main

import (
	"fmt"
	"github.com/imakiri/golang-stepik/testlib/working"
	"os"
	"time"
)

func MustNewTest(units []interface{}) working.Test {
	var t, err = working.NewTest(nil, units, 10*time.Second, 10*time.Millisecond, []string{})
	if err != nil {
		panic(err)
	}

	return t
}

var feedback_command = "The program should print back only the given command and no more"

func main() {
	working.Run(os.Stdin, os.Stdout, os.Stderr, MustNewTest([]interface{}{
		working.Output{
			Expected: "Write how many cups of coffee you will need:",
			Feedback: "aa",
		},
		working.Input{Command: fmt.Sprintf("%d", 25)},
		working.Output{
			Expected: fmt.Sprintf("For %d cups of coffee you will need:", 25),
			Feedback: "b",
		},
		working.Output{
			Expected: fmt.Sprintf("%d ml of water", 200*25),
			Feedback: "c",
		},
		working.Output{
			Expected: fmt.Sprintf("%d ml of milk", 50*25),
			Feedback: "d",
		},
		working.Output{
			Expected: fmt.Sprintf("%d g of coffee beans", 15*25),
			Feedback: "e",
		},
	}))
}
