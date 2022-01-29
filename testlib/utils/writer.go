package utils

import "io"

type ttpWriter struct {
	w []io.Writer
}

func (t *ttpWriter) Write(p []byte) (n int, err error) {
	p = append([]byte("> "), p...)
	for i := range t.w {
		n, err = t.w[i].Write(p)
		if err != nil {
			return
		}
		if n != len(p) {
			err = io.ErrShortWrite
			return
		}
	}
	return len(p), nil
}

func NewTTPWriter(writers ...io.Writer) io.Writer {
	allWriters := make([]io.Writer, 0, len(writers))
	for _, w := range writers {
		allWriters = append(allWriters, w)
	}
	return &ttpWriter{allWriters}
}
