package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/md5"
	"encoding/hex"
	"bytes"
	"github.com/beego/beego/v2/server/web"
)

type BaseController struct {
	web.Controller
	controllerName string
	actionName string
}

type MainController struct {
	BaseController
}

type LoginController struct {
	BaseController
}

type AdminController struct {
	BaseController
}

var admin_id string
var admin_pw string
var app_name string
var auth_key string
var auth_crypt_key string
var flag string

func AesEncrypt(origData, key []byte) ([]byte, error) {
	padded_key := Padding(key, 16)
	block, err := aes.NewCipher(padded_key)
	if err != nil {
		return nil, err
	}
	blockSize := block.BlockSize()
	origData = Padding(origData, blockSize)
	blockMode := cipher.NewCBCEncrypter(block, padded_key[:blockSize])
	crypted := make([]byte, len(origData))
	blockMode.CryptBlocks(crypted, origData)
	return crypted, nil
}

func Padding(ciphertext []byte, blockSize int) []byte {
	padding := blockSize - len(ciphertext)%blockSize
	padtext := bytes.Repeat([]byte{byte(padding)}, padding)
	return append(ciphertext, padtext...)
}

func Md5(s string) string {
	h := md5.New()
	h.Write([]byte(s))
	return hex.EncodeToString(h.Sum(nil))
}

func (this *BaseController) Prepare() {
	controllerName, _ := this.GetControllerAndAction()
	session := this.Ctx.GetCookie(Md5("sess"))

	if controllerName == "MainController" {
		if session == "" || session != Md5(admin_id + auth_key) {
			this.Redirect("/login/login", 403)
			return
		}
	} else if controllerName == "LoginController" {
		if session != "" {
			this.Ctx.SetCookie(Md5("sess"), "")
		}
	} else if controllerName == "AdminController" {
		domain := this.Ctx.Input.Domain()

		if domain != "localhost" {
			this.Abort("Not Local")
			return
		}
	}
}

func (this *MainController) Index() {
	this.TplName = "index.html"
	this.Data["app_name"] = app_name
	this.Data["flag"] = flag
	this.Render()
}

func (this *LoginController) Login() {
	this.TplName = "login.html"
	this.Data["app_name"] = app_name
	this.Render()
}

func (this *LoginController) Auth() {
	id := this.GetString("id")
	password := this.GetString("password")

	if id == admin_id && password == admin_pw {
		this.Ctx.SetCookie(Md5("sess"), Md5(admin_id + auth_key), 300)

		this.Ctx.WriteString("<script>alert('Login Success');location.href='/main/index';</script>")
		return
	}
	this.Ctx.WriteString("<script>alert('Login Fail');location.href='/login/login';</script>")
}

func (this *AdminController) AuthKey() {
	encrypted_auth_key, _ := AesEncrypt([]byte(auth_key), []byte(auth_crypt_key))
	this.Ctx.WriteString(hex.EncodeToString(encrypted_auth_key))
}

func main() {
	app_name, _ = web.AppConfig.String("app_name")
	auth_key, _ = web.AppConfig.String("auth_key")
	auth_crypt_key, _ = web.AppConfig.String("auth_crypt_key")
	admin_id, _ = web.AppConfig.String("id")
	admin_pw, _ = web.AppConfig.String("password")
	flag, _ = web.AppConfig.String("flag")

	web.AutoRouter(&MainController{})
	web.AutoRouter(&LoginController{})
	web.AutoRouter(&AdminController{})
	web.Run()
}