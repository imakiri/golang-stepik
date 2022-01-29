package runner

import (
	"errors"
	"fmt"
	"github.com/imakiri/golang-stepik/testlib/butler"
	"github.com/imakiri/golang-stepik/testlib/utils"
	"gopkg.in/yaml.v2"
	"io"
	"os"
	"os/exec"
	"time"
)

type Runner interface {
	Run(debug bool) (message Message, err error)
}

type runner struct {
	exe bool
	std struct {
		in  io.Reader
		out io.Writer
	}
	tester   *exec.Cmd
	solution *exec.Cmd
	buffers  struct {
		ttp *utils.Buffer
		ptt *utils.Buffer
		all *utils.Buffer
	}
	err     io.ReadCloser
	timeout time.Duration
}

func (r *runner) shutdown() {
	r.exe = false
	r.solution.Process.Kill()
	r.tester.Process.Kill()
}

func (r *runner) state() chan Message {
	var ch = make(chan Message, 1)

	go func() {
		var message = new(Message)

		var err = yaml.NewDecoder(r.err).Decode(message)
		if err != nil {
			message.Error += fmt.Sprintf("\ndecoder error: %s", err)
		}

		ch <- *message
	}()

	return ch
}

func (r *runner) Run(debug bool) (message Message, err error) {
	var tester butler.Butler
	if tester, err = butler.NewButler(butler.Tester); err != nil {
		return
	}
	defer tester.Tidy()

	var solution butler.Butler
	if debug {
		if solution, err = butler.NewButler(butler.ReferenceSolution); err != nil {
			return
		}
	} else {
		if solution, err = butler.NewButler(butler.UserSolution); err != nil {
			return
		}
	}
	defer solution.Tidy()

	var pr, pw = io.Pipe()
	var tr, tw = io.Pipe()

	var writers_ptt = io.MultiWriter(r.buffers.all, r.buffers.ptt)
	var writers_ttp = utils.NewTTPWriter(r.buffers.all, r.buffers.ttp)

	if r.tester, err = tester.Prepare(nil, io.TeeReader(pr, writers_ptt), tw, nil); err != nil {
		return
	}
	if r.solution, err = solution.Prepare(nil, io.TeeReader(tr, writers_ttp), pw, nil); err != nil {
		return
	}
	if r.err, err = r.tester.StderrPipe(); err != nil {
		return
	}

	r.exe = true
	if err = r.solution.Start(); err != nil {
		return
	}
	if err = r.tester.Start(); err != nil {
		return
	}
	defer r.shutdown()

	var ch = r.state()
	if debug {
		defer io.Copy(r.std.out, r.buffers.all)
	}

	select {
	case message := <-ch:
		return message, nil
	case <-time.After(r.timeout):
		var message = Message{
			Result:   false,
			Feedback: "",
			Error:    "",
		}
		return message, errors.New("error: tester timeout")
	}
}

func NewRunner(timeout time.Duration) (*runner, error) {
	var ur = new(runner)
	ur.buffers.ptt = new(utils.Buffer)
	ur.buffers.ttp = new(utils.Buffer)
	ur.buffers.all = new(utils.Buffer)
	ur.timeout = timeout
	ur.std.in = os.Stdin
	ur.std.out = os.Stdout
	return ur, nil
}
