package working

import (
	"github.com/imakiri/golang-stepik/testlib/runner"
	"gopkg.in/yaml.v2"
	"io"
	"time"
)

func Run(in io.ReadCloser, out io.WriteCloser, err io.WriteCloser, tests []Test) {
	var handler = new(handler)
	handler.in = in
	handler.out = out
	handler.err = err
	defer handler.Close()

	var message = new(runner.Message)
	message.Result = true

	for i := range tests {
		var ch = make(chan bool, 1)
		go func() {
			time.Sleep(tests[i].Delay())
			ch <- tests[i].Test(handler)
		}()

		var result bool
		select {
		case result = <-ch:
		case <-time.After(tests[i].Timeout()):
			result = false
		}

		if result {
			continue
		} else {
			message.Result = false
			message.Feedback = tests[i].Feedback()

			var err = tests[i].Error()
			if err != nil {
				message.Error = err.Error()
			}
		}
	}

	var encoder = yaml.NewEncoder(err)
	defer encoder.Close()

	encoder.Encode(message)
}
