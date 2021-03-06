package butler

import (
	"errors"
	"fmt"
	"io"
	"os"
	"os/exec"
	"time"
)

type golang struct {
	name string
}

func (g *golang) compile() error {
	var goRoot = os.Getenv("GOROOT")
	var compiler = exec.Command(fmt.Sprintf("%s\\bin\\go.exe", goRoot), "build", fmt.Sprintf("%s.go", g.name))
	var err = compiler.Run()
	if err != nil {
		var output, err = compiler.Output()
		if err != nil {
			return err
		}
		return errors.New(string(output))
	}

	return nil
}

func (g *golang) cleanup(filename string) error {
	var err error
	for start := time.Now(); time.Since(start) < time.Second; {
		if err = os.Remove(filename); err == nil {
			break
		}
	}
	return err
}

func (g *golang) Prepare(args []string, in io.Reader, out io.Writer, err io.Writer) (*exec.Cmd, error) {
	var e = g.compile()
	if e != nil {
		return nil, e
	}

	var h = exec.Command(g.name, args...)

	if in != nil {
		h.Stdin = in
	}
	if out != nil {
		h.Stdout = out
	}
	if err != nil {
		h.Stderr = err
	}

	return h, nil
}

func (g *golang) Tidy() error {
	var err error
	for start := time.Now(); time.Since(start) < time.Second; {
		if err = os.Remove(fmt.Sprintf("%s.exe", g.name)); err == nil {
			break
		}
	}
	return err
}

func newGolang(name string) *golang {
	var g = new(golang)
	g.name = name
	return g
}
