package route

import (
	_ "embed"
	"fmt"
	"html/template"
	"loginme/structs"
	"loginme/templates"
	"strconv"

	"github.com/gin-gonic/gin"
)

func Index(c *gin.Context) {
	c.HTML(200, "index.tmpl", gin.H{
		"title": "Try Loginme",
	})
}

func Login(c *gin.Context) {
	idString, flag := c.GetQuery("id")
	if !flag {
		idString = "1"
	}
	id, err := strconv.Atoi(idString)
	if err != nil {
		id = 1
	}
	TargetUser := structs.Admin
	for _, user := range structs.Users {
		if user.Id == id {
			TargetUser = user
		}
	}

	age := TargetUser.Age
	if age == "" {
		age, flag = c.GetQuery("age")
		if !flag {
			age = "forever 18 (Tell me the age)"
		}
	}

	if err != nil {
		c.AbortWithError(500, err)
	}

	html := fmt.Sprintf(templates.AdminIndexTemplateHtml, age)
	if err != nil {
		c.AbortWithError(500, err)
	}

	tmpl, err := template.New("admin_index").Parse(html)
	if err != nil {
		c.AbortWithError(500, err)
	}

	tmpl.Execute(c.Writer, TargetUser)
}
