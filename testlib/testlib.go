package testlib

import (
	"errors"
	"fmt"
	"os"
	"os/exec"
	"strings"
	"time"
)

const (
	userSourceCode    = "main.go"
	userProgramName   = "main.exe"
	testerSourceCode  = "tester.go"
	testerProgramName = "tester.exe"
)

type Runner interface {
	Run() (result bool, feedback string, err error)
}

type Main struct{}

func (m *Main) compile(filename string, targetname string) error {
	var compiler = exec.Command("E:\\golang\\sdk\\go1.16.10\\bin\\go.exe", "build", "-o", targetname, filename)
	var err = compiler.Run()
	if err != nil {
		return err
	}

	if !compiler.ProcessState.Success() {
		fmt.Println(compiler.String())

		var output, err = compiler.Output()
		if err != nil {
			return err
		}
		return errors.New(string(output))
	}

	return nil
}

func (m *Main) cleanup(filename string) error {
	var err error
	for start := time.Now(); time.Since(start) < time.Second; {
		if err = os.Remove(filename); err == nil {
			break
		}
	}
	return err
}

func (m *Main) Supervise() {
	var err = m.compile(userSourceCode, userProgramName)
	if err != nil {
		fmt.Println(err)
		return
	}

	if err = m.compile(testerSourceCode, testerProgramName); err != nil {
		fmt.Println(err)
		return
	}

	var runner Runner
	if runner, err = NewUnirunner(5 * time.Second); err != nil {
		fmt.Println(err)
		return
	}

	var result bool
	var feedback string
	result, feedback, err = runner.Run()
	fmt.Printf("\n--------------\n"+
		"result: %v\nfeedback: %v\nerror: %v", result, strings.TrimSpace(feedback), err)

	if err = m.cleanup(userProgramName); err != nil {
		fmt.Println(err)
		return
	}
	if err = m.cleanup(testerProgramName); err != nil {
		fmt.Println(err)
		return
	}
}

func (m *Main) Execute(tests []Test) {
	var err = m.compile(userSourceCode, userProgramName)
	if err != nil {
		fmt.Println(err)
		return
	}

	var runner Runner
	if runner, err = NewRunner(tests, userProgramName); err != nil {
		fmt.Println(err)
		return
	}

	var result bool
	var feedback string
	result, feedback, err = runner.Run()
	fmt.Print(result, feedback, err)

	if err = m.cleanup(userProgramName); err != nil {
		fmt.Println(err)
		return
	}
}
