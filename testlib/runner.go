package testlib

import "fmt"

type Tester interface {
	Test() (result bool, feedback string)
}

type runner struct {
	tester Tester
}

func (r *runner) Run() {
	fmt.Print(r.tester.Test())
}

func NewRunner(tests []Test) *runner {
	var r = new(runner)
	var err error
	if r.tester, err = NewTester(tests); err != nil {
		panic(err)
	}

	return r
}
