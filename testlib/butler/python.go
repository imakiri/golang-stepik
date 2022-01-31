package butler

import (
	"io"
	"os/exec"
)

type python struct {
	filename string
}

func (p *python) Prepare(args []string, in io.Reader, out io.Writer, err io.Writer) (*exec.Cmd, error) {
	panic("implement me")
}

func (p *python) Tidy() error {
	panic("implement me")
}

func newPython(t string) *python {
	var p = new(python)
	//p.filename = fmt.Sprintf("%s.exe", t)
	return p
}
