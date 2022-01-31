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

const UserSolution string = "user"
const ReferenceSolution string = "main"

type Butler interface {
	Prepare(args []string, in io.Reader, out io.Writer, err io.Writer) (*exec.Cmd, error)
	Tidy() error
}

func NewButler(target string) (Butler, error) {
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
	var name string
	for _, file := range files {
		if !file.Mode().IsRegular() {
			continue
		}

		if strings.HasPrefix(file.Name(), target) {
			ext = filepath.Ext(file.Name())
			name = strings.TrimSuffix(file.Name(), ext)
		}
	}

	switch ext {
	case ".go":
		b = newGolang(name)
	case ".py":
		b = newPython(name)
	default:
		return nil, fmt.Errorf("unsupported file extension: %s", ext)
	}

	return b, nil
}
