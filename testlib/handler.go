package testlib

import (
	"bufio"
	"bytes"
	"fmt"
	"github.com/golang-collections/go-datastructures/bitarray"
	"io"
	"os"
	"os/exec"
)

type handler struct {
	exe        bool
	program    *exec.Cmd
	traceBuf   *buffer
	stdin      io.Writer
	stdout     io.Reader
	stdoutPipe struct {
		reader *io.PipeReader
		writer *io.PipeWriter
	}
	bitarray bitarray.BitArray
	index    uint64
}

func (h *handler) Read(p []byte) (n int, err error) {
	return h.stdoutPipe.reader.Read(p)
}

func (h *handler) Write(p []byte) (n int, err error) {
	n, err = io.MultiWriter(h.traceBuf, h.stdin, os.Stdout).Write(p)
	h.index += uint64(n)
	return
}

func (h *handler) Close() error {
	h.exe = false
	return h.program.Process.Kill()
}

func (h *handler) Buffer() (*bytes.Buffer, bitarray.BitArray, uint64) {
	return &h.traceBuf.buf, h.bitarray, h.index
}

func (h *handler) run() {
	h.exe = true
	var reader = bufio.NewReader(h.stdout)
	var writer = io.MultiWriter(h.stdoutPipe.writer, h.traceBuf, os.Stdout)
	for h.exe {
		var b, err = reader.ReadByte()
		if err != nil {
			return
		}

		var _, _ = writer.Write([]byte{b})
		h.bitarray.SetBit(h.index)
		h.index++

		//var n, err = io.Copy(writer, reader)
		//
		//if err != nil {
		//	return
		//}
		//for i := h.index; i < uint64(n); i++ {
		//	h.bitarray.SetBit(i)
		//}
		//h.index += uint64(n)

		//select {
		//case exe = <-h.state:
		//default:
		//	for exe {
		//		select {
		//		case e := <-h.state:
		//			exe = e
		//		case b := <- stream:
		//			writer.Write([]byte{b})
		//			h.bitarray.SetBit(h.index)
		//			h.index++
		//		}
		//	}
		//}
	}
}

func NewHandler(filename string, args []string) (*handler, error) {
	var h = new(handler)
	h.program = exec.Command(fmt.Sprintf("./%s", filename), args...)
	h.traceBuf = newBuffer()
	h.stdoutPipe.reader, h.stdoutPipe.writer = io.Pipe()
	h.bitarray = bitarray.NewSparseBitArray()

	var err error
	if h.stdin, err = h.program.StdinPipe(); err != nil {
		return nil, err
	}
	if h.stdout, err = h.program.StdoutPipe(); err != nil {
		return nil, err
	}
	if err = h.program.Start(); err != nil {
		return nil, err
	}

	go h.run()
	return h, nil
}
