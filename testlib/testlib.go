package testlib

import (
	"fmt"
	"github.com/imakiri/golang-stepik/testlib/cfg"
	"github.com/imakiri/golang-stepik/testlib/runner"
	"github.com/kr/pretty"
	"time"
)

type Main struct{}

func (m *Main) Supervise(debug bool) {
	var config, err = cfg.ReadConfig()
	if err != nil {
		fmt.Println(err)
		return
	}

	pretty.Println(*config)

	switch config.Mode {
	case cfg.Main:
		m.main(config)
	case cfg.Legacy:
		m.legacy(config)
	default:
		fmt.Printf("error: unknown mode: %s\n", config.Mode)
	}
}

func (m *Main) main(config *cfg.Config) {
	var r, err = runner.NewRunner(15 * time.Second)

	if err != nil {
		fmt.Println(err)
		return
	}

	if err = r.Run(*config); err != nil {
		fmt.Println("Supervisor message:")
		fmt.Printf("\t%v\n", err)
	}
}

func (m *Main) legacy(config *cfg.Config) {

}
