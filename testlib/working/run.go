package working

import (
	"github.com/imakiri/golang-stepik/testlib/runner"
	"gopkg.in/yaml.v2"
	"io"
	"time"
)

func Run(in io.ReadCloser, out io.WriteCloser, err io.WriteCloser, test Test) {
	var handler = new(handler)
	handler.in = in
	handler.out = out
	handler.err = err
	defer handler.Close()

	var message = new(runner.Message)
	message.Result = true

	var ch = make(chan bool, 1)
	go func() {
		time.Sleep(test.Delay())
		ch <- test.Test(handler)
	}()

	var result bool
	select {
	case result = <-ch:
	case <-time.After(test.Timeout()):
		result = false
	}

	if !result {
		message.Result = false
		message.Feedback = test.Feedback()

		var err = test.Error()
		if err != nil {
			message.Error = err.Error()
		}
	}

	var encoder = yaml.NewEncoder(err)
	defer encoder.Close()

	encoder.Encode(message)
}
