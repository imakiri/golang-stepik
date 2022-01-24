package testlib

import (
	"fmt"
	"io"
	"os/exec"
)

type handler struct {
	exe     bool
	program *exec.Cmd
	stdin   io.WriteCloser
	stdout  *buffer
	buffers struct {
		in    *buffer
		out   *buffer
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
	h.stdin.Close()
	h.exe = false
	return err
}

func (h *handler) Buffers() (trace *buffer, in *buffer, out *buffer, err error) {
	if h.exe {
		return nil, nil, nil, fmt.Errorf("the program is stil running")
	}
	return h.buffers.trace, h.buffers.in, h.buffers.out, nil
}

func NewHandler(filename string, args []string) (*handler, error) {
	var h = new(handler)
	h.buffers.trace = new(buffer)
	h.buffers.in = new(buffer)
	h.buffers.out = new(buffer)
	h.program = exec.Command(fmt.Sprintf("./%s", filename), args...)

	var stdin, err = h.program.StdinPipe()
	if err != nil {
		return nil, err
	}
	h.stdin = stdin
	h.stdout = new(buffer)

	var writer = io.MultiWriter(h.stdout, h.buffers.out, h.buffers.trace)
	h.program.Stdout = writer
	h.program.Stderr = writer

	if err = h.program.Start(); err != nil {
		return nil, err
	}

	return h, nil
}
