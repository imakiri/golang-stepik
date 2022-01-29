package testlib

import (
	"fmt"
	"github.com/imakiri/golang-stepik/testlib/runner"
	"reflect"
	"time"
)

type Main struct{}

func (m *Main) Supervise(debug bool) {
	fmt.Printf("\n--------------\n")
	var r, err = runner.NewRunner(15 * time.Second)

	if err != nil {
		fmt.Println(err)
		return
	}

	var message runner.Message
	message, err = r.Run(debug)
	fmt.Printf("\n--------------\n")

	var me = reflect.ValueOf(&message).Elem()
	var _type = me.Type()

	fmt.Println("Tester message:")
	for i := 0; i < me.NumField(); i++ {
		f := me.Field(i)
		fmt.Printf("\t%s: %v\n", _type.Field(i).Name, f.Interface())
	}

	fmt.Println("Supervisor message:")
	fmt.Printf("\t%v\n", err)
}
