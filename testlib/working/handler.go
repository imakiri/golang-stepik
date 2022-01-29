package working

import "io"

type handler struct {
	in  io.ReadCloser
	out io.WriteCloser
	err io.WriteCloser
}

func (h *handler) Read(p []byte) (n int, err error) {
	return h.in.Read(p)
}

func (h *handler) Write(p []byte) (n int, err error) {
	return h.out.Write(p)
}

func (h *handler) Close() error {
	h.out.Close()
	h.err.Close()
	return nil
}
