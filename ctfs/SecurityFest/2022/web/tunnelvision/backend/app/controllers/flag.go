package controllers

import (
	"github.com/revel/revel"
	"os"
)

type Flag struct {
	*revel.Controller
}

func (c Flag) Index() revel.Result {
	var flag = os.Getenv("FLAG")
	return c.Render(flag)
}
