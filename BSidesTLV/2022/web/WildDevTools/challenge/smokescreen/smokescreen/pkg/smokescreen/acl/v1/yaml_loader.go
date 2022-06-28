package acl

import (
	"errors"
	"fmt"
	"io/ioutil"
	"os"

	"gopkg.in/yaml.v2"
)

type YAMLLoader struct {
	path string
}

func NewYAMLLoader(path string) *YAMLLoader {
	return &YAMLLoader{path}
}

type YAMLConfig struct {
	Services        []YAMLRule `yaml:"services"`
	Default         *YAMLRule  `yaml:"default"`
	Version         string     `yaml:"version"`
	GlobalDenyList  []string   `yaml:"global_deny_list"`  // domains which will be blocked even in report mode
	GlobalAllowList []string   `yaml:"global_allow_list"` // domains which will be allowed for every host type
}

type YAMLRule struct {
	Name         string   `yaml:"name"`
	Project      string   `yaml:"project"` // owner
	Action       string   `yaml:"action"`
	AllowedHosts []string `yaml:"allowed_domains"`
}

func (yc *YAMLConfig) ValidateConfig() error {
	_, err := yc.Load()
	return err
}

func (yl *YAMLLoader) Load() (*ACL, error) {
	f, err := os.Open(yl.path)
	if err != nil {
		return nil, err
	}
	defer f.Close()

	yamlFile, err := ioutil.ReadAll(f)
	if err != nil {
		return nil, fmt.Errorf("could not load acl configuration")
	}

	yamlConfig := YAMLConfig{}
	err = yaml.Unmarshal(yamlFile, &yamlConfig)
	if err != nil {
		return nil, err
	}

	if yamlConfig.Version != "v1" {
		return nil, fmt.Errorf("expected version \"v1\" got %#v", yamlConfig.Version)
	}

	return yamlConfig.Load()
}

func (cfg *YAMLConfig) Load() (*ACL, error) {
	acl := ACL{
		Rules: make(map[string]Rule),
	}

	if cfg.Services == nil {
		return nil, errors.New("Top level list 'services' is missing")
	}

	for _, v := range cfg.Services {
		p, err := PolicyFromAction(v.Action)
		if err != nil {
			return nil, err
		}

		r := Rule{
			Project:     v.Project,
			Policy:      p,
			DomainGlobs: v.AllowedHosts,
		}

		err = acl.Add(v.Name, r)
		if err != nil {
			return nil, err
		}
	}

	if cfg.Default != nil {
		p, err := PolicyFromAction(cfg.Default.Action)
		if err != nil {
			return nil, err
		}

		acl.DefaultRule = &Rule{
			Project:     cfg.Default.Project,
			Policy:      p,
			DomainGlobs: cfg.Default.AllowedHosts,
		}
	}

	acl.GlobalAllowList = []string{}
	acl.GlobalDenyList = []string{}

	if cfg.GlobalAllowList != nil {
		acl.GlobalAllowList = cfg.GlobalAllowList
	}
	if cfg.GlobalDenyList != nil {
		acl.GlobalDenyList = cfg.GlobalDenyList
	}

	return &acl, nil
}
