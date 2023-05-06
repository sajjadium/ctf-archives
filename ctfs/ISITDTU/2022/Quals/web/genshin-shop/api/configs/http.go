package configs

import "fmt"

type Http struct {
	Host   string `yaml:"host"`
	Port   uint   `yaml:"port"`
	Origin string `yaml:"origin"`
}

func (s *Http) ToString() string {
	return fmt.Sprintf("%s:%d", s.Host, s.Port)
}
