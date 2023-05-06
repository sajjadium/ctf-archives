package main

import (
	"context"
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"html/template"
	"log"
	"net/http"
	"os"
	"regexp"
	"strconv"
	"sync"
	"time"

	"github.com/chromedp/cdproto/cdp"
	"github.com/chromedp/cdproto/network"
	"github.com/chromedp/chromedp"

	"github.com/gin-contrib/sessions"
	"github.com/gin-contrib/sessions/cookie"
	"github.com/gin-gonic/gin"
)

type User struct {
	username string
	password string
	Notes    []string
}

var users = make(map[string]*User)
var adminToken string
var networkAddr string
var lastRequestTime int64 = 0
var lastRequestTimeLock = sync.Mutex{}

func init() {
	t := make([]byte, 8)
	if _, err := rand.Read(t); err != nil {
		panic(err)
	}
	adminToken = hex.EncodeToString(t)
	var ok bool
	if networkAddr, ok = os.LookupEnv("networkAddr"); !ok {
		panic("require networkAddr")
	}
	fmt.Printf("admin token: %s\n", adminToken)
	fmt.Printf("network addr: %s\n", networkAddr)
}

func login(c *gin.Context) {
	username := c.PostForm("username")
	password := c.PostForm("password")
	if (!regexp.MustCompile("^[a-zA-Z0-9]+$").MatchString(username)) || username == "" || len(username) > 16 {
		c.JSON(http.StatusBadRequest, gin.H{"ok": false, "message": "invalid username"})
		return
	}
	if password == "" || len(password) > 16 {
		c.JSON(http.StatusBadRequest, gin.H{"ok": false, "message": "invalid password"})
		return
	}
	if user, ok := users[username]; ok {
		if user.password != password {
			c.JSON(http.StatusForbidden, gin.H{"ok": false, "message": "login failed"})
			return
		} else {
			session := sessions.Default(c)
			session.Set("username", username)
			session.Save()
			c.JSON(http.StatusOK, gin.H{"ok": true, "message": "success"})
			return
		}
	} else {
		users[username] = &User{username: username, password: password}
		session := sessions.Default(c)
		session.Set("username", username)
		session.Save()
		c.JSON(http.StatusOK, gin.H{"ok": true, "message": "success"})
		return
	}
}

func postNotes(c *gin.Context) {
	if !c.GetBool("is_login") {
		c.JSON(http.StatusForbidden, gin.H{"ok": false, "message": "login first"})
		return
	}
	user := c.MustGet("user").(*User)
	content := c.PostForm("content")
	if len(content) > 1024 {
		c.JSON(http.StatusOK, gin.H{"ok": false, "message": "content too long"})
		return
	}
	user.Notes = append(user.Notes, content)
	c.JSON(http.StatusOK, gin.H{"ok": true, "message": "success"})
}

func viewPage(c *gin.Context) {
	if !c.GetBool("is_login") {
		c.Redirect(http.StatusFound, "/login")
	} else {
		var user *User
		if c.GetBool("is_admin") {
			username := c.Query("username")
			var ok bool
			if user, ok = users[username]; !ok {
				c.AbortWithError(500, fmt.Errorf("user does not exist"))
				return
			}
		} else {
			user = c.MustGet("user").(*User)
		}
		i, _ := strconv.Atoi(c.Param("id"))
		if len(user.Notes) <= i {
			c.AbortWithError(500, fmt.Errorf("note does not exist"))
			return
		}
		note := user.Notes[i]
		c.HTML(200, "view.html", template.HTML(note))
	}
}

func indexPage(c *gin.Context) {
	if !c.GetBool("is_login") {
		c.Redirect(http.StatusFound, "/login")
	} else {
		c.HTML(200, "index.html", c.MustGet("user"))
	}
}

func loginPage(c *gin.Context) {
	c.HTML(200, "login.html", nil)
}

func AuthRequired() gin.HandlerFunc {
	return func(c *gin.Context) {
		session := sessions.Default(c)
		if token, err := c.Cookie("admin_token"); err == nil {
			if token == adminToken {
				c.Set("user", &User{"admin", "password", []string{}})
				c.Set("is_admin", true)
				c.Set("is_login", true)
				c.Next()
				return
			}
		}
		username := session.Get("username")
		if username == nil {
			c.Set("is_login", false)
			c.Next()
			return
		}
		if user, ok := users[username.(string)]; !ok {
			c.Set("is_login", false)
			c.Next()
			return
		} else {
			c.Set("user", user)
			c.Set("is_admin", false)
			c.Set("is_login", true)
			c.Next()
		}
	}
}

func withCSP() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Header("Content-Security-Policy", "default-src 'self'; base-uri 'none'; object-src 'none';")
		c.Header("X-Content-Type-Options", "nosniff")
		c.Next()
	}
}

func SetCookie(name, value, domain, path string, httpOnly bool) chromedp.Action {
	return chromedp.ActionFunc(func(ctx context.Context) error {
		expr := cdp.TimeSinceEpoch(time.Now().Add(24 * time.Hour))
		err := network.SetCookie(name, value).
			WithExpires(&expr).
			WithDomain(domain).
			WithPath(path).
			WithHTTPOnly(httpOnly).
			Do(ctx)
		if err != nil {
			return err
		}
		return nil
	})
}

func sendToAdmin(c *gin.Context) {
	lastRequestTimeLock.Lock()
	if time.Now().Unix()-lastRequestTime < 20 {
		lastRequestTimeLock.Unlock()
		c.JSON(http.StatusOK, gin.H{"ok": false, "message": "please try again after 20 seconds"})
		return
	}
	lastRequestTime = time.Now().Unix()
	lastRequestTimeLock.Unlock()

	id := c.PostForm("id")
	user := c.MustGet("user").(*User)

	opts := append(chromedp.DefaultExecAllocatorOptions[:],
		chromedp.Flag("headless", "chrome"),
		chromedp.Flag("disable-gpu", true),
		chromedp.Flag("no-sandbox", true),
		chromedp.Flag("disable-setuid-sandbox", true),
		chromedp.Flag("js-flags", "--noexpose_wasm,--jitless"),
		chromedp.Flag("disable-extensions", false),
		chromedp.Flag("enable-features", "BlockInsecurePrivateNetworkRequests,PrivateNetworkAccessRespectPreflightResults"),
		chromedp.Flag("load-extension", "./proxy_blocker"),
	)

	allocCtx, cancel := chromedp.NewExecAllocator(context.Background(), opts...)
	defer cancel()
	ctx, cancel := chromedp.NewContext(allocCtx, chromedp.WithLogf(log.Printf))
	defer cancel()
	ctx, cancel = context.WithTimeout(ctx, 5*time.Second)
	defer cancel()

	if err := chromedp.Run(ctx,
		SetCookie("admin_token", adminToken, networkAddr, "/", true),
		chromedp.Navigate("http://"+networkAddr+":8888/view/"+id+"?username="+user.username),
		chromedp.Sleep(3*time.Second),
	); err != nil {
		c.JSON(http.StatusOK, gin.H{"ok": false, "message": err.Error()})
		fmt.Printf("chromedp error: %v\n", err)
		return
	}
	c.JSON(http.StatusOK, gin.H{"ok": true, "message": "success"})
}

func main() {
	gin.SetMode(gin.ReleaseMode)
	r := gin.Default()
	secret := make([]byte, 8)
	if _, err := rand.Read(secret); err != nil {
		panic(err)
	}
	store := cookie.NewStore(secret)
	r.Use(sessions.Sessions("session", store))
	r.Use(gin.Recovery())
	r.Static("/static", "./static")
	r.LoadHTMLGlob("./template/*")
	r.POST("/api/login", login)
	r.POST("/api/post", AuthRequired(), postNotes)
	r.POST("/api/sendToAdmin", AuthRequired(), sendToAdmin)
	r.GET("/", withCSP(), AuthRequired(), indexPage)
	r.GET("/login", withCSP(), loginPage)
	r.GET("/view/:id", withCSP(), AuthRequired(), viewPage)
	err := r.Run(":8080")
	if err != nil {
		fmt.Printf("start server failed: %s", err.Error())
	}
}
