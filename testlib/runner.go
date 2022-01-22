package testlib

import (
	"fmt"
	"os"
	"os/exec"
	"time"
)

type Tester interface {
	Test(filename string) (result bool, feedback string, err error)
}

type runner struct {
	tester Tester
}

func (r *runner) Run() {
	var output, err = exec.Command("E:\\golang\\sdk\\go1.16.10\\bin\\go.exe", "build", "main.go").CombinedOutput()
	if err != nil {
		fmt.Println(string(output))
		fmt.Println(err)
		return
	}

	var result bool
	var feedback string
	result, feedback, err = r.tester.Test("main.exe")
	fmt.Println()
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

func NewRunner(tests []Test) *runner {
	var r = new(runner)
	var err error
	if r.tester, err = NewTester(tests); err != nil {
		panic(err)
	}

	return r
}
