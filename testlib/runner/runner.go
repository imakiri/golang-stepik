package runner

import (
	"errors"
	"fmt"
	"github.com/imakiri/golang-stepik/testlib/butler"
	"github.com/imakiri/golang-stepik/testlib/cfg"
	"github.com/imakiri/golang-stepik/testlib/utils"
	"gopkg.in/yaml.v2"
	"io"
	"os"
	"os/exec"
	"reflect"
	"strings"
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

func (r *runner) print(message *Message) {
	var me = reflect.ValueOf(message).Elem()
	var _type = me.Type()

	fmt.Println("\nTester message:")
	for i := 0; i < me.NumField(); i++ {
		f := me.Field(i)
		fmt.Printf("\t%s: %v\n", _type.Field(i).Name, f.Interface())
	}
}

func (r *runner) run(debug bool, args []string, tester, solution butler.Butler) (message Message, err error) {
	var pr, pw = io.Pipe()
	var tr, tw = io.Pipe()

	var writers_ptt = io.MultiWriter(r.buffers.all, r.buffers.ptt)
	var writers_ttp = utils.NewTTPWriter(r.buffers.all, r.buffers.ttp)

	if r.tester, err = tester.Prepare(nil, io.TeeReader(pr, writers_ptt), tw, nil); err != nil {
		return
	}
	if r.solution, err = solution.Prepare(args, io.TeeReader(tr, writers_ttp), pw, nil); err != nil {
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
		defer io.Copy(r.std.out, strings.NewReader("\n--------------\n"))
		defer io.Copy(r.std.out, r.buffers.all)
		defer io.Copy(r.std.out, strings.NewReader("--------------\n"))
		defer io.Copy(r.std.out, strings.NewReader("Test sequence:\n"))
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

func (r *runner) Run(config cfg.Config) error {
	var err error
	var solution butler.Butler
	if config.Debug {
		if solution, err = butler.NewButler(butler.ReferenceSolution); err != nil {
			return err
		}
	} else {
		if solution, err = butler.NewButler(butler.UserSolution); err != nil {
			return err
		}
	}
	defer solution.Tidy()

	var tester butler.Butler
	var message = new(Message)
	for _, test := range config.Tests {
		fmt.Print("---------------------------------------\n")
		fmt.Printf("Starting %s\n\n", test.Name)

		if tester, err = butler.NewButler(test.Name); err != nil {
			return err
		}

		var args = strings.Split(test.Args, " ")
		if *message, err = r.run(config.Debug, args, tester, solution); err != nil {
			tester.Tidy()
			return err
		}
		tester.Tidy()

		r.print(message)

		if !message.Result && !config.Debug {
			return nil
		}
	}

	return nil
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
