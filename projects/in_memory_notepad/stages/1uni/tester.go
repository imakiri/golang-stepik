package main

import (
	"fmt"
	"github.com/imakiri/golang-stepik/testlib"
	"github.com/imakiri/golang-stepik/testlib/working"
	"io"
	"os"
	"time"
)

func MustNewTest(units []interface{}) testlib.Test {
	var t, err = working.NewTest(nil, units, time.Second, 10*time.Millisecond, []string{})
	if err != nil {
		panic(err)
	}

	return t
}

var feedback_command = "The program should print back only the given command and no more"

var tests = []testlib.Test{
	MustNewTest([]interface{}{
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
	}),
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
	os.Exit(0)
	return nil
}

func main() {
	var handler = new(handler)
	handler.in = os.Stdin
	handler.out = os.Stdout
	handler.err = os.Stderr
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
