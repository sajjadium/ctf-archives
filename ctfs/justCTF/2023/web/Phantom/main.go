package main

import (
	"bytes"
	"crypto/rand"
	"fmt"
	"html/template"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strings"

	recaptcha "github.com/dpapathanasiou/go-recaptcha"
	"github.com/google/uuid"
	"github.com/gorilla/csrf"
	"github.com/gorilla/mux"
	"github.com/gorilla/sessions"
	"golang.org/x/net/html"
)

func generateSecret(length int) []byte {
	token := make([]byte, length)
	_, err := rand.Read(token)
	if err != nil {
		fmt.Println(err)
		return nil
	}
	return token
}

var store = sessions.NewCookieStore(generateSecret(32))

const templateDir = "templates"

var templates = template.Must(template.ParseFiles(
	filepath.Join(templateDir, "header.html"),
	filepath.Join(templateDir, "footer.html"),
	filepath.Join(templateDir, "signup.html"),
	filepath.Join(templateDir, "login.html"),
	filepath.Join(templateDir, "profile.html"),
	filepath.Join(templateDir, "edit.html"),
	filepath.Join(templateDir, "index.html"),
	filepath.Join(templateDir, "bot.html"),
))

type User struct {
	ID          uuid.UUID
	Username    string
	Password    string
	Name        string
	Description string
}

var Users map[string]*User

func isSafeHTML(input string) bool {
	var buffer bytes.Buffer
	tokenizer := html.NewTokenizer(strings.NewReader(input))

	for {
		tt := tokenizer.Next()
		switch {
		case tt == html.ErrorToken:
			return true
		case tt == html.StartTagToken, tt == html.EndTagToken, tt == html.SelfClosingTagToken:
			token := tokenizer.Token()
			if len(token.Attr) > 0 {
				return false
			}

			switch token.Data {
			case "h1", "h2", "h3", "h4", "h5", "h6", "b", "i", "a", "img", "p", "code", "svg", "textarea":
				buffer.WriteString(token.String())
			default:
				return false
			}
		case tt == html.TextToken:
			buffer.WriteString(tokenizer.Token().String())
		default:
			return false
		}
	}
}

func indexHandler(w http.ResponseWriter, r *http.Request) {
	templates.ExecuteTemplate(w, "index", nil)
}

func signupHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == http.MethodGet {
		data := map[string]interface{}{
			"csrfToken": csrf.Token(r),
		}
		templates.ExecuteTemplate(w, "signup", data)
	} else if r.Method == http.MethodPost {
		username := r.FormValue("username")
		password := r.FormValue("password")
		name := r.FormValue("name")

		if _, ok := Users[username]; ok {
			http.Error(w, "Username is already taken", http.StatusConflict)
			return
		}

		Users[username] = &User{ID: uuid.New(), Username: username, Password: password, Name: name}
		http.Redirect(w, r, "/login", http.StatusFound)
	}
}

func profileHandler(w http.ResponseWriter, r *http.Request) {
	session, _ := store.Get(r, "session")
	if auth, ok := session.Values["authenticated"].(bool); !ok || !auth {
		http.Error(w, "Forbidden", http.StatusForbidden)
		return
	}
	username := session.Values["username"].(string)
	if user, ok := Users[username]; ok {
		data := map[string]interface{}{
			"Name":        user.Name,
			"Description": template.HTML(user.Description),
		}
		templates.ExecuteTemplate(w, "profile", data)
	} else {
		http.Error(w, "Unauthenticated", http.StatusUnauthorized)
		return
	}
}

func profileEditHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == http.MethodGet {
		session, _ := store.Get(r, "session")
		if auth, ok := session.Values["authenticated"].(bool); !ok || !auth {
			http.Error(w, "Forbidden", http.StatusForbidden)
			return
		}
		username := session.Values["username"].(string)
		if user, ok := Users[username]; ok {
			data := map[string]interface{}{
				"User":      user,
				"csrfToken": csrf.Token(r),
			}
			templates.ExecuteTemplate(w, "edit", data)
		} else {
			http.Error(w, "Unauthenticated", http.StatusUnauthorized)
			return
		}
	} else {
		// handle file upload
		session, _ := store.Get(r, "session")
		if auth, ok := session.Values["authenticated"].(bool); !ok || !auth {
			http.Error(w, "Forbidden", http.StatusForbidden)
			return
		}
		name := r.FormValue("name")
		description := r.FormValue("description")

		username := session.Values["username"].(string)
		if user, ok := Users[username]; ok {

			if isSafeHTML(description) {
				descriptionHTML, err := html.Parse(strings.NewReader(description))
				var buf bytes.Buffer
				html.Render(&buf, descriptionHTML)

				if err != nil {
					http.Error(w, "Forbidden", http.StatusForbidden)
				}
				if len(name) > 0 {
					user.Name = name
				}
				user.Description = buf.String()

				data := map[string]interface{}{
					"Name":        user.Name,
					"Description": template.HTML(user.Description),
				}
				templates.ExecuteTemplate(w, "profile", data)
			} else {
				http.Error(w, "Forbidden", http.StatusForbidden)
				return
			}
		}
	}
}

func loginHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == http.MethodGet {
		data := map[string]interface{}{
			"csrfToken": csrf.Token(r),
		}
		templates.ExecuteTemplate(w, "login", data)
	} else if r.Method == http.MethodPost {
		username := r.FormValue("username")
		password := r.FormValue("password")
		if user, ok := Users[username]; ok {
			if user.Password == password {
				session, _ := store.Get(r, "session")
				session.Values["authenticated"] = true
				session.Values["username"] = user.Username
				session.Save(r, w)
				http.Redirect(w, r, "/profile", http.StatusFound)
				return
			} else {

			}
		} else {
			data := map[string]interface{}{
				"Error":     "Invalid username or password",
				"csrfToken": csrf.Token(r),
			}
			templates.ExecuteTemplate(w, "login", data)
		}
	}
}

func logoutHandler(w http.ResponseWriter, r *http.Request) {
	session, _ := store.Get(r, "session")
	session.Values["authenticated"] = false
	session.Save(r, w)
}

func botHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == http.MethodGet {
		data := map[string]interface{}{
			"csrfToken": csrf.Token(r),
		}
		templates.ExecuteTemplate(w, "bot", data)
	} else if r.Method == http.MethodPost {
		clientIP := r.RemoteAddr
		recaptchaResponse := r.FormValue("g-recaptcha-response")
		url := r.FormValue("url")
		success, err := recaptcha.Confirm(clientIP, recaptchaResponse)
		if err != nil {
			http.Error(w, "Failed to verify reCAPTCHA", http.StatusInternalServerError)
			return
		}

		if !success {
			http.Error(w, "reCAPTCHA failed", http.StatusBadRequest)
			return
		}
		cmd := exec.Command("./bot", "-url", url)
		cmd.Start()
		data := map[string]interface{}{
			"Success":   "URL has been submitted",
			"csrfToken": csrf.Token(r),
		}
		templates.ExecuteTemplate(w, "bot", data)

	}
}

func main() {
	Users = make(map[string]*User)
	recaptcha.Init(os.Getenv("GRECAPTCHA"))
	CSRF := csrf.Protect(generateSecret(32))
	store.Options = &sessions.Options{
		Path:     "/",
		MaxAge:   86400 * 7,
		HttpOnly: true,
		SameSite: http.SameSiteNoneMode,
		Secure:   true,
	}
	r := mux.NewRouter()
	r.HandleFunc("/signup", signupHandler)
	r.HandleFunc("/profile", profileHandler)
	r.HandleFunc("/profile/edit", profileEditHandler)
	r.HandleFunc("/login", loginHandler)
	r.HandleFunc("/logout", logoutHandler)
	r.HandleFunc("/bot", botHandler)
	r.HandleFunc("/", indexHandler)
	http.ListenAndServe(":8000", CSRF(r))
}
