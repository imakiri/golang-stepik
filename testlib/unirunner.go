package testlib

import (
	"bufio"
	"errors"
	"fmt"
	"io"
	"os"
	"os/exec"
	"time"
)

type handle struct {
	process *exec.Cmd
	std     struct {
		in  io.WriteCloser
		out io.ReadCloser
		err io.ReadCloser
	}
}

func NewHandel(filename string, args []string) (*handle, error) {
	var h = new(handle)
	h.process = exec.Command(filename, args...)

	return h, nil
}

type unirunner struct {
	exe bool
	std struct {
		in  io.Reader
		out io.Writer
	}
	tester  *handle
	program *handle
	buffers struct {
		//err *buffer
		ttp *buffer
		ptt *buffer
		all *buffer
	}
	err     io.Reader
	timeout time.Duration
}

func (ur *unirunner) shutdown() {
	ur.exe = false
	ur.program.process.Process.Kill()
	ur.tester.process.Process.Kill()
}

//func (ur *unirunner) ttp() {
//	var writers = io.MultiWriter(ur.buffers.all, ur.buffers.ttp, ur.program.std.in, ur.std.out)
//	var reader = bufio.NewReader(ur.tester.buffers.out)
//	for ur.exe {
//		var _, err = reader.WriteTo(writers)
//		if err != nil {
//			ur.shutdown()
//			return
//		}
//	}
//}

//func (ur *unirunner) ptp() {
//	var writers = io.MultiWriter(ur.buffers.all, ur.buffers.ptt, ur.tester.std.in, ur.std.out)
//	var reader = bufio.NewReader(ur.program.buffers.out)
//	for ur.exe {
//		var _, err = reader.WriteTo(writers)
//		if err != nil {
//			ur.shutdown()
//			return
//		}
//	}
//}

type feedback struct {
	ok       bool
	feedback string
	err      error
}

func (ur *unirunner) state() chan feedback {
	var ch = make(chan feedback, 1)

	go func() {
		var reader = bufio.NewScanner(ur.err)
		var feedback feedback
		var readOk bool
	loop:
		for {
			for reader.Scan() {
				fmt.Fprintln(ur.std.out, reader.Text())
				if !readOk {
					switch reader.Text() {
					case "true", "True":
						feedback.ok = true
						break loop
					case "false", "False":
						feedback.ok = false
						readOk = true
					default:
						feedback.err = fmt.Errorf("unsupported feedback format for ok value, got: %s", reader.Text())
						break loop
					}
				} else {
					feedback.feedback += reader.Text() + "\n"
				}
			}
			break
		}

		ch <- feedback
	}()

	return ch
}

func (ur *unirunner) Run() (result bool, feedback string, err error) {
	if ur.program, err = NewHandel("main.exe", nil); err != nil {
		return false, "", err
	}
	if ur.tester, err = NewHandel("tester.exe", nil); err != nil {
		return false, "", err
	}

	var pr, pw = io.Pipe()
	var tr, tw = io.Pipe()
	ur.program.process.Stdout = pw
	ur.tester.process.Stdout = tw
	var writers_ptt = io.MultiWriter(ur.buffers.all, ur.buffers.ptt, ur.std.out)
	var writers_ttp = io.MultiWriter(ur.buffers.all, ur.buffers.ttp, ur.std.out)
	ur.tester.process.Stdin = io.TeeReader(pr, writers_ptt)
	ur.program.process.Stdin = io.TeeReader(tr, writers_ttp)
	//var errbuf = new(buffer)
	var er, ew = io.Pipe()
	ur.tester.process.Stderr = ew
	//ur.tester.process.Stderr = errbuf
	ur.err = er
	//ur.err = errbuf

	ur.exe = true
	if err = ur.program.process.Start(); err != nil {
		return false, "", err
	}
	if err = ur.tester.process.Start(); err != nil {
		return false, "", err
	}
	defer ur.shutdown()

	//go ur.ptp()
	//go ur.ttp()

	var ch = ur.state()
	select {
	case feedback := <-ch:
		return feedback.ok, feedback.feedback, feedback.err
	case <-time.After(ur.timeout):
		return false, "", errors.New("tester timeout")
	}
}

func NewUnirunner(timeout time.Duration) (*unirunner, error) {
	var ur = new(unirunner)
	//ur.buffers.err = new(buffer)
	ur.buffers.ptt = new(buffer)
	ur.buffers.ttp = new(buffer)
	ur.buffers.all = new(buffer)
	ur.timeout = timeout

	ur.std.in = os.Stdin
	ur.std.out = os.Stdout

	return ur, nil
}
