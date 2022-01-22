package testlib

import (
	"fmt"
	"io"
	"os/exec"
)

type handler struct {
	exe bool
	//state   chan bool
	//stop    chan struct{}
	program *exec.Cmd
	stdin   io.WriteCloser
	stdout  *buffer
	buffers struct {
		in    *bufferW
		out   *bufferW
		trace *buffer
	}

	error error
}

func (h *handler) Read(p []byte) (n int, err error) {
	return h.stdout.Read(p)
}

func (h *handler) Write(p []byte) (n int, err error) {
	h.buffers.trace.Write([]byte("> " + string(p)))
	h.buffers.in.Write([]byte("> " + string(p)))
	return h.stdin.Write(p)
}

func (h *handler) Close() error {
	var err = h.program.Process.Kill()
	h.exe = false
	return err
}

func (h *handler) Dump() (*bufferW, *bufferW, error) {
	if h.exe {
		return nil, nil, fmt.Errorf("the program is stil running")
	}
	return h.buffers.in, h.buffers.out, nil
}

func (h *handler) Trace() (*buffer, error) {
	if h.exe {
		return nil, fmt.Errorf("the program is stil running")
	}
	return h.buffers.trace, nil
}

func NewHandler(filename string, args []string) (*handler, error) {
	var h = new(handler)
	//h.stop = make(chan struct{}, 1)
	//h.state = make(chan bool, 1)
	h.buffers.trace = NewBuffer()
	h.buffers.in = NewBufferW(2000)
	h.buffers.out = NewBufferW(2000)
	h.program = exec.Command(fmt.Sprintf("./%s", filename), args...)

	var stdin, err = h.program.StdinPipe()
	if err != nil {
		return nil, err
	}
	h.stdin = stdin
	h.stdout = NewBuffer()

	var writer = io.MultiWriter(h.stdout, h.buffers.out, h.buffers.trace)
	h.program.Stdout = writer
	h.program.Stderr = writer

	if err = h.program.Start(); err != nil {
		return nil, err
	}

	return h, nil
}
