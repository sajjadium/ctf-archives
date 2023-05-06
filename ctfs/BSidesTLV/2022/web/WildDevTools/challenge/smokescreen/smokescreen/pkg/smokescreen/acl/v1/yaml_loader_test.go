package acl

import (
	"testing"

	"github.com/sirupsen/logrus"
	"github.com/stretchr/testify/assert"
)

func TestYAMLLoader(t *testing.T) {
	a := assert.New(t)

	// Load a sane config
	{
		yl := NewYAMLLoader("testdata/sample_config.yaml")
		acl, err := New(logrus.New(), yl, []string{})
		a.Nil(err)
		a.NotNil(acl)
		a.Equal(4, len(acl.Rules))
		a.Equal(0, len(acl.GlobalDenyList))
		a.Equal(0, len(acl.GlobalAllowList))
	}

	// Load a sane config with global lists
	{
		yl := NewYAMLLoader("testdata/sample_config_with_global.yaml")
		acl, err := New(logrus.New(), yl, []string{})
		a.Nil(err)
		a.NotNil(acl)
		a.Equal(4, len(acl.Rules))
		a.Equal(3, len(acl.GlobalDenyList))
		a.Equal(4, len(acl.GlobalAllowList))
	}

	// Load a broken config
	{
		yl := NewYAMLLoader("testdata/broken_config.yaml")
		acl, err := New(logrus.New(), yl, []string{})
		a.NotNil(err)
		a.Nil(acl)
	}

	// Load a config that contains an unknown action
	{
		yl := NewYAMLLoader("testdata/unknown_action.yaml")
		acl, err := New(logrus.New(), yl, []string{})
		a.NotNil(err)
		a.Nil(acl)
	}
}

func TestYAMLLoaderInvalidGlob(t *testing.T) {
	a := assert.New(t)

	yl := NewYAMLLoader("testdata/contains_invalid_glob.yaml")
	acl, err := New(logrus.New(), yl, []string{})
	a.NotNil(err)
	a.Nil(acl)
}

func TestYAMLLoaderInvalidMiddleGlob(t *testing.T) {
	a := assert.New(t)

	yl := NewYAMLLoader("testdata/contains_middle_glob.yaml")
	acl, err := New(logrus.New(), yl, []string{})
	a.NotNil(err)
	a.Nil(acl)
}

func TestYAMLLoaderDisabledAclAction(t *testing.T) {
	a := assert.New(t)
	disabledActions := []string{"enforce"}
	yl := NewYAMLLoader("testdata/sample_config.yaml")
	acl, err := New(logrus.New(), yl, disabledActions)
	a.NotNil(err)
	a.Nil(acl)
}
