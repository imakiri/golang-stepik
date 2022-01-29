package butler

import (
	"fmt"
	"io"
	"io/fs"
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
)

type target string

const UserSolution target = "user"
const ReferenceSolution target = "main"
const Tester target = "tester"

type Butler interface {
	Prepare(args []string, in io.Reader, out io.Writer, err io.Writer) (*exec.Cmd, error)
	Tidy() error
}

func NewButler(t target) (Butler, error) {
	var b Butler

	var wd, err = os.Getwd()
	if err != nil {
		return nil, err
	}


	var files []fs.FileInfo
	if files, err = ioutil.ReadDir(wd); err != nil {
		return nil, err
	}

	var ext string
	for _, file := range files {
		if !file.Mode().IsRegular() {
			continue
		}

		if strings.HasPrefix(file.Name(), string(t)) {
			ext = filepath.Ext(file.Name())
		}
	}

	switch ext {
	case ".go":
		b = newGolang(t)
	case ".python":
		b = newPython(t)
	default:
		return nil, fmt.Errorf("unsupported file extension: %s", ext)
	}

	return b, nil
}