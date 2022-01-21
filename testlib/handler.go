package testlib

import (
	"io"
	"os/exec"
)

type handler struct {
	program *exec.Cmd
	stdin   io.WriteCloser
	stdout  io.ReadCloser
}

func (h *handler) Read(p []byte) (n int, err error) {
	return h.stdout.Read(p)
}

func (h *handler) Write(p []byte) (n int, err error) {
	return h.stdin.Write(p)
}

func (h *handler) WriteString(s string) (n int, err error) {
	var b = []byte(s)
	return h.Write(b)
}

func (h *handler) Close() error {
	h.stdin.Close()
	h.stdout.Close()
	return h.program.Process.Kill()
}

func NewHandler(args []string) (*handler, error) {
	var program = exec.Command("./main.exe", args...)

	var h = new(handler)
	h.program = program

	var err error
	if h.stdin, err = program.StdinPipe(); err != nil {
		return nil, err
	}
	if h.stdout, err = program.StdoutPipe(); err != nil {
		return nil, err
	}
	if err = program.Start(); err != nil {
		return nil, err
	}

	return h, nil
}
