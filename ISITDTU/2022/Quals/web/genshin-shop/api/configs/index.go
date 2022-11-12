package configs

import (
	"os"

	"gopkg.in/yaml.v3"
)

type YamlConfig struct {
	Http     Http     `yaml:"http"`
	MySql    MySql    `yaml:"mysql"`
	ChromeDp ChromeDp `yaml:"chrome_dp"`
	Flag     Flag     `yaml:"flag"`
}

var _default *YamlConfig

// Load config from file path.
func loadConfig(path string) (*YamlConfig, error) {

	// Create config structure.
	config := &YamlConfig{}

	// Open config file.
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	// Init new YAML decode.
	d := yaml.NewDecoder(file)

	// Start YAML decoding from file.
	if err := d.Decode(&config); err != nil {
		return nil, err
	}

	return config, nil
}

func Default() (*YamlConfig, error) {
	if _default == nil {
		var e error
		_default, e = loadConfig("config.yml")
		if e != nil {
			return nil, e
		}
	}
	return _default, nil
}
