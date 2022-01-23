package testlib

import (
	"bytes"
	"sync"
	_ "unsafe"
)

type buffer struct {
	sync.Mutex
	bytes.Buffer
}

func (b *buffer) Read(p []byte) (n int, err error) {
	b.Lock()
	defer b.Unlock()
	return b.Buffer.Read(p)
}

func (b *buffer) Write(p []byte) (n int, err error) {
	b.Lock()
	defer b.Unlock()
	return b.Buffer.Write(p)
}

//go:noescape
//go:linkname nanotime runtime.nanotime
func nanotime() int64

type bufferR struct {
	sync.Mutex
	bytes.Buffer
	monotime []int64
}

func (b *bufferR) Read(p []byte) (n int, err error) {
	b.Lock()
	defer b.Unlock()
	n, err = b.Buffer.Read(p)
	for i := 0; i < n; i++ {
		b.monotime = append(b.monotime, nanotime())
	}
	return
}

func (b *bufferR) Write(p []byte) (n int, err error) {
	b.Lock()
	defer b.Unlock()
	return b.Buffer.Write(p)
}
func NewBufferR(size int) *bufferR {
	var b = new(bufferR)
	b.monotime = make([]int64, 0, size)
	return b
}

type bufferW struct {
	sync.Mutex
	bytes.Buffer
	monotime []int64
}

func (b *bufferW) Read(p []byte) (n int, err error) {
	b.Lock()
	defer b.Unlock()
	return b.Buffer.Read(p)
}

func (b *bufferW) Write(p []byte) (n int, err error) {
	b.Lock()
	defer b.Unlock()
	n, err = b.Buffer.Write(p)
	for i := 0; i < n; i++ {
		b.monotime = append(b.monotime, nanotime())
	}
	return
}

func NewBufferW(size int) *bufferW {
	var b = new(bufferW)
	b.monotime = make([]int64, 0, size)
	return b
}
