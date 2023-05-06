package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"text/template"

	"github.com/golang-jwt/jwt"
)

type Account struct {
	id         string
	pw         string
	is_admin   bool
	secret_key string
}

type AccountClaims struct {
	Id       string `json:"id"`
	Is_admin bool   `json:"is_admin"`
	jwt.StandardClaims
}

type Resp struct {
	Status bool   `json:"status"`
	Msg    string `json:"msg"`
}

type TokenResp struct {
	Status bool   `json:"status"`
	Token  string `json:"token"`
}

var acc []Account
var secret_key = os.Getenv("KEY")
var flag = os.Getenv("FLAG")
var admin_id = os.Getenv("ADMIN_ID")
var admin_pw = os.Getenv("ADMIN_PW")

func clear_account() {
	acc = acc[:1]
}

func get_account(uid string) Account {
	for i := range acc {
		if acc[i].id == uid {
			return acc[i]
		}
	}
	return Account{}
}

func jwt_encode(id string, is_admin bool) (string, error) {
	claims := AccountClaims{
		id, is_admin, jwt.StandardClaims{},
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString([]byte(secret_key))
}

func jwt_decode(s string) (string, bool) {
	token, err := jwt.ParseWithClaims(s, &AccountClaims{}, func(token *jwt.Token) (interface{}, error) {
		return []byte(secret_key), nil
	})
	if err != nil {
		fmt.Println(err)
		return "", false
	}
	if claims, ok := token.Claims.(*AccountClaims); ok && token.Valid {
		return claims.Id, claims.Is_admin
	}
	return "", false
}

func auth_handler(w http.ResponseWriter, r *http.Request) {
	uid := r.FormValue("id")
	upw := r.FormValue("pw")
	if uid == "" || upw == "" {
		return
	}
	if len(acc) > 1024 {
		clear_account()
	}
	user_acc := get_account(uid)
	if user_acc.id != "" && user_acc.pw == upw {
		token, err := jwt_encode(user_acc.id, user_acc.is_admin)
		if err != nil {
			return
		}
		p := TokenResp{true, token}
		res, err := json.Marshal(p)
		if err != nil {
		}
		w.Write(res)
		return
	}
	w.WriteHeader(http.StatusForbidden)
	return
}

func regist_handler(w http.ResponseWriter, r *http.Request) {
	uid := r.FormValue("id")
	upw := r.FormValue("pw")

	if uid == "" || upw == "" {
		return
	}

	if get_account(uid).id != "" {
		w.WriteHeader(http.StatusForbidden)
		return
	}
	if len(acc) > 4 {
		clear_account()
	}
	new_acc := Account{uid, upw, false, secret_key}
	acc = append(acc, new_acc)

	p := Resp{true, ""}
	res, err := json.Marshal(p)
	if err != nil {
	}
	w.Write(res)
	return
}

func flag_handler(w http.ResponseWriter, r *http.Request) {
	token := r.Header.Get("X-Token")
	if token != "" {
		id, is_admin := jwt_decode(token)
		if is_admin == true {
			p := Resp{true, "Hi " + id + ", flag is " + flag}
			res, err := json.Marshal(p)
			if err != nil {
			}
			w.Write(res)
			return
		} else {
			w.WriteHeader(http.StatusForbidden)
			return
		}
	}
}

func root_handler(w http.ResponseWriter, r *http.Request) {
	token := r.Header.Get("X-Token")
	if token != "" {
		id, _ := jwt_decode(token)
		acc := get_account(id)
		tpl, err := template.New("").Parse("Logged in as " + acc.id)
		if err != nil {
		}
		tpl.Execute(w, &acc)
	} else {

		return
	}
}

func main() {
	admin := Account{admin_id, admin_pw, true, secret_key}
	acc = append(acc, admin)

	http.HandleFunc("/", root_handler)
	http.HandleFunc("/auth", auth_handler)
	http.HandleFunc("/flag", flag_handler)
	http.HandleFunc("/regist", regist_handler)
	log.Fatal(http.ListenAndServe("0.0.0.0:11000", nil))
}
