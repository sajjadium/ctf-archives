package configs

import "fmt"

type ChromeDp struct {
	Host     string `yaml:"host"`
	Port     uint   `yaml:"port"`
	Lifespan uint   `yaml:"lifespan"`
}

func (c *ChromeDp) ToString() string {
	return fmt.Sprintf("ws://%s:%d", c.Host, c.Port)
}
