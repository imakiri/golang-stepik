package cfg

import (
	"gopkg.in/yaml.v2"
	"os"
)

type mode string

const (
	Main   mode = "main"
	Legacy mode = "legacy"
)

type Config struct {
	Mode  mode
	Debug bool
	Tests []struct {
		Name string
		Args string
	}
}

func ReadConfig() (*Config, error) {
	var f, err = os.Open("config.yaml")
	if err != nil {
		return nil, err
	}

	var conf = new(Config)
	if err = yaml.NewDecoder(f).Decode(conf); err != nil {
		return nil, err
	}

	return conf, nil
}
