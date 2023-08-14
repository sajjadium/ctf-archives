package controller

import (
	"bytes"
	"crypto/md5"
	"crypto/rand"
	"encoding/base64"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"math"
	"net/http"
	"regexp"

	"golang.org/x/crypto/bcrypt"

	"github.com/golang-jwt/jwt"
	"github.com/val1d/bb_ctf/api"
	"github.com/val1d/bb_ctf/db"
)

const userDataQery = `query {
	user(username: "%s") {
	  id
	  username
	  name
	  intro
	  reputation
	  rank
	}
  }`

func bindAndValidateLoginRequest(r *http.Request) (api.LoginRequest, error) {
	var req api.LoginRequest
	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		return req, err
	}

	if *req.Password == "" || *req.Username == "" {
		return req, fmt.Errorf("empty username or password")
	}

	return req, nil
}

func getRandomString(l int) string {
	buff := make([]byte, int(math.Ceil(float64(l)/float64(1.33333333333))))
	rand.Read(buff)
	str := base64.RawURLEncoding.EncodeToString(buff)
	return str[:l]
}

func (s *server) PostUserLogin(w http.ResponseWriter, r *http.Request) {
	req, err := bindAndValidateLoginRequest(r)
	if err != nil {
		api.HandleError(err, w)
		return
	}

	var user db.Users
	res := s.db.Impl.Find(&user, "username = ?", req.Username)

	if res.RowsAffected != 1 {
		api.HandleNotFound(w)
		return
	}

	err = bcrypt.CompareHashAndPassword(user.Password, []byte(*req.Password))
	if err != nil {
		api.HandleError(err, w)
		return
	}

	t := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{"user_id": user.ID})
	jwtStr, _ := t.SignedString([]byte(api.JwtSecret))

	authToken := api.AuthToken{Token: &jwtStr}

	api.EncodeResponse(w, authToken)
}

func verifyValidator(v string) bool {
	m, err := regexp.MatchString("^[a-zA-Z0-9=]{30,40}$", v)
	if err != nil {
		return false
	}
	if m {
		return true
	} else {
		return false
	}
}

func (s *server) PostUserRegister(w http.ResponseWriter, r *http.Request) {
	req, err := bindAndValidateLoginRequest(r)
	if err != nil {
		api.HandleError(err, w)
		return
	}

	var user db.Users
	res := s.db.Impl.Find(&user, "username = ?", req.Username)

	if res.RowsAffected >= 1 {
		api.HandleError(fmt.Errorf("user already exists"), w)
		return
	}

	hash, err := bcrypt.GenerateFromPassword([]byte(*req.Password), bcrypt.DefaultCost)
	if err != nil {
		api.HandleError(err, w)
		return
	}

	user = db.Users{Username: *req.Username, Password: hash, Reputation: 0, Pow: getRandomString(9)}

	result := s.db.Impl.Create(&user)

	if result.Error != nil || result.RowsAffected != 1 {
		api.HandleError(fmt.Errorf("error creating user"), w)
		return
	}

	t := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{"user_id": user.ID})
	jwtStr, _ := t.SignedString([]byte(api.JwtSecret))

	authToken := api.AuthToken{Token: &jwtStr}

	api.EncodeResponse(w, authToken)
}

func bindAndValidateImportRepoRequest(r *http.Request) (api.ImportRepoRequest, error) {
	var req api.ImportRepoRequest
	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		return req, err
	}

	if req.Username == nil || *req.Username == "" {
		return req, fmt.Errorf("empty username")
	}

	if req.Validator == nil || *req.Validator == "" {
		return req, fmt.Errorf("empty validator")
	}

	if !verifyValidator(*req.Validator) {
		return req, fmt.Errorf("invalid validator format")
	}

	return req, nil
}

func (s *server) PostUserImportReputation(w http.ResponseWriter, r *http.Request) {
	req, err := bindAndValidateImportRepoRequest(r)
	if err != nil {
		api.HandleError(err, w)
		return
	}

	userID := getUserID(r)

	var user db.Users
	s.db.Impl.Find(&user, "id = ?", userID)

	postBody, _ := json.Marshal(map[string]string{
		"query": fmt.Sprintf(userDataQery, *req.Username),
	})

	resp, err := http.Post("https://hackerone.com/graphql", "application/json", bytes.NewBuffer(postBody))

	if err != nil {
		api.HandleError(err, w)
		return
	}

	if resp.StatusCode != 200 {
		api.HandleError(fmt.Errorf("non-200 status code: %d", resp.StatusCode), w)
		return
	}

	defer resp.Body.Close()

	type respData struct {
		Data struct {
			User struct {
				Reputation int
				Intro      string
			}
		}
	}

	var rd respData

	err = json.NewDecoder(resp.Body).Decode(&rd)

	if err != nil {
		api.HandleError(fmt.Errorf("error parsing h1 response: %v", err), w)
		return
	}

	if rd.Data.User.Reputation == 0 || rd.Data.User.Intro == "" {
		api.HandleError(fmt.Errorf("bad response from h1"), w)
		return
	}

	if rd.Data.User.Intro != *req.Validator {
		api.HandleError(fmt.Errorf("incorrect validator"), w)
		return
	}

	user.Reputation = uint64(rd.Data.User.Reputation)
	s.db.Impl.Save(&user)
}

func getMD5(text string) string {
	hash := md5.Sum([]byte(text))
	return hex.EncodeToString(hash[:])
}

func (s *server) GetUserInfo(w http.ResponseWriter, r *http.Request) {
	userID := getUserID(r)

	var user db.Users
	s.db.Impl.Find(&user, "id = ?", userID)

	resp := api.UserInfoResponse{Username: &user.Username, Reputation: &user.Reputation, Pow: api.Ptr(user.Pow[:5]), Md5: api.Ptr(getMD5(user.Pow))}

	api.EncodeResponse(w, resp)
}
