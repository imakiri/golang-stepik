package testlib

import (
	"bytes"
	"sync"
)

type buffer struct {
	mutex sync.Mutex
	buf   bytes.Buffer
}

func (b *buffer) Read(p []byte) (n int, err error) {
	b.mutex.Lock()
	defer b.mutex.Unlock()
	return b.buf.Read(p)
}

func (b *buffer) Write(p []byte) (n int, err error) {
	b.mutex.Lock()
	defer b.mutex.Unlock()
	return b.buf.Write(p)
}

func newBuffer() *buffer {
	var b = new(buffer)
	return b
}
