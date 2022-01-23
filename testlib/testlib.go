package testlib

import (
	"fmt"
	"os"
	"os/exec"
	"time"
)

type Runner interface {
	Run() (result bool, feedback string, err error)
}

type main struct {
	tests []Test
}

func (r *main) Execute() {
	var compiler = exec.Command("E:\\golang\\sdk\\go1.16.10\\bin\\go.exe", "build", "main.go")
	var err = compiler.Run()
	if err != nil {
		fmt.Println(err)
		return
	}

	if !compiler.ProcessState.Success() {
		fmt.Println(compiler.String())

		var output, err = compiler.Output()
		if err != nil {
			fmt.Println(err)
			return
		}
		fmt.Println(string(output))
		return
	}

	var tester *runner
	if tester, err = NewRunner(r.tests, "main.exe"); err != nil {
		fmt.Println(err)
		return
	}

	var result bool
	var feedback string
	result, feedback, err = tester.Run()
	fmt.Print(result, feedback, err)

	for start := time.Now(); time.Since(start) < time.Second; {
		if err = os.Remove("main.exe"); err == nil {
			break
		}
	}

	if err != nil {
		fmt.Println(err)
	}
}

func NewMain(tests []Test) *main {
	var r = new(main)
	r.tests = tests
	return r
}
