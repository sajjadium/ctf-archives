package main

import (
	"log"
	"os"

	"github.com/gin-contrib/static"
	"github.com/gin-gonic/gin"
	"github.com/gin-gonic/gin/binding"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

type Vulnerability struct {
	gorm.Model
	Name string
	Logo string
	URL  string
}

func main() {
	gin.SetMode(gin.ReleaseMode)

	flag := os.Getenv("FLAG")
	if flag == "" {
		flag = "SECCON{dummy_flag}"
	}

	db, err := gorm.Open(sqlite.Open(":memory:"), &gorm.Config{})
	if err != nil {
		log.Fatal("failed to connect database")
	}

	db.AutoMigrate(&Vulnerability{})
	db.Create(&Vulnerability{Name: "Heartbleed", Logo: "/images/heartbleed.png", URL: "https://heartbleed.com/"})
	db.Create(&Vulnerability{Name: "Badlock", Logo: "/images/badlock.png", URL: "http://badlock.org/"})
	db.Create(&Vulnerability{Name: "DROWN Attack", Logo: "/images/drown.png", URL: "https://drownattack.com/"})
	db.Create(&Vulnerability{Name: "CCS Injection", Logo: "/images/ccs.png", URL: "http://ccsinjection.lepidum.co.jp/"})
	db.Create(&Vulnerability{Name: "httpoxy", Logo: "/images/httpoxy.png", URL: "https://httpoxy.org/"})
	db.Create(&Vulnerability{Name: "Meltdown", Logo: "/images/meltdown.png", URL: "https://meltdownattack.com/"})
	db.Create(&Vulnerability{Name: "Spectre", Logo: "/images/spectre.png", URL: "https://meltdownattack.com/"})
	db.Create(&Vulnerability{Name: "Foreshadow", Logo: "/images/foreshadow.png", URL: "https://foreshadowattack.eu/"})
	db.Create(&Vulnerability{Name: "MDS", Logo: "/images/mds.png", URL: "https://mdsattacks.com/"})
	db.Create(&Vulnerability{Name: "ZombieLoad Attack", Logo: "/images/zombieload.png", URL: "https://zombieloadattack.com/"})
	db.Create(&Vulnerability{Name: "RAMBleed", Logo: "/images/rambleed.png", URL: "https://rambleed.com/"})
	db.Create(&Vulnerability{Name: "CacheOut", Logo: "/images/cacheout.png", URL: "https://cacheoutattack.com/"})
	db.Create(&Vulnerability{Name: "SGAxe", Logo: "/images/sgaxe.png", URL: "https://cacheoutattack.com/"})
	db.Create(&Vulnerability{Name: flag, Logo: "/images/" + flag + ".png", URL: "seccon://" + flag})

	r := gin.Default()

	//	Return a list of vulnerability names
	//	{"Vulnerabilities": ["Heartbleed", "Badlock", ...]}
	r.GET("/api/vulnerabilities", func(c *gin.Context) {
		var vulns []Vulnerability
		if err := db.Where("name != ?", flag).Find(&vulns).Error; err != nil {
			c.JSON(400, gin.H{"Error": "DB error"})
			return
		}
		var names []string
		for _, vuln := range vulns {
			names = append(names, vuln.Name)
		}
		c.JSON(200, gin.H{"Vulnerabilities": names})
	})

	//	Return details of the vulnerability
	//	{"Logo": "???.png", "URL": "https://..."}
	r.POST("/api/vulnerability", func(c *gin.Context) {
		//	Validate the parameter
		var json map[string]interface{}
		if err := c.ShouldBindBodyWith(&json, binding.JSON); err != nil {
			c.JSON(400, gin.H{"Error": "JSON error 1"})
			return
		}
		if name, ok := json["Name"]; !ok || name == "" || name == nil {
			c.JSON(400, gin.H{"Error": "no \"Name\""})
			return
		}

		//	Get details of the vulnerability
		var query Vulnerability
		if err := c.ShouldBindBodyWith(&query, binding.JSON); err != nil {
			c.JSON(400, gin.H{"Error": "JSON error 2"})
			return
		}
		var vuln Vulnerability
		if err := db.Where(&query).First(&vuln).Error; err != nil {
			c.JSON(404, gin.H{"Error": "not found"})
			return
		}

		c.JSON(200, gin.H{
			"Logo": vuln.Logo,
			"URL":  vuln.URL,
		})
	})

	r.Use(static.Serve("/", static.LocalFile("static", false)))

	if err := r.Run(":8080"); err != nil {
		log.Fatal(err)
	}
}
