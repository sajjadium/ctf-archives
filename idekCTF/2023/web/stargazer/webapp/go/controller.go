package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"

	"github.com/google/uuid"
	"github.com/gorilla/sessions"
	"github.com/labstack/echo-contrib/session"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	"golang.org/x/exp/slices"
)

func loginHandler(c echo.Context) error {
	user := new(User)
	if err := c.Bind(user); err != nil {
		return err
	}

	res, err := loginUser(user)
	if err != nil {
		return err
	}

	if res == 0 {
		return c.JSON(400, map[string]interface{}{
			"err":     "Something is invalid",
			"message": "Username / Password is Invalid",
		})
	}

	sess, _ := session.Get("session", c)
	sess.Options = &sessions.Options{
		Path:     "/",
		MaxAge:   86400 * 7,
		HttpOnly: true,
	}
	sess.Values["loggedIn"] = true
	sess.Values["username"] = user.Username
	sess.Save(c.Request(), c.Response())

	return c.JSON(http.StatusOK, map[string]interface{}{
		"message": "success",
		"path":    "/myfiles",
	})
}

func registerHandler(c echo.Context) error {
	user := new(User)
	if err := c.Bind(user); err != nil {
		return err
	}

	if len(user.Username) < 8 || len(user.Password) < 8 {
		return c.JSON(400, map[string]interface{}{
			"err":     "Something is Invalid",
			"message": "Username and Password Less Than 8",
		})
	}

	err := registerUser(user.Username, user.Password)
	if err != nil {
		return err
	}

	sess, _ := session.Get("session", c)
	sess.Options = &sessions.Options{
		Path:     "/",
		MaxAge:   86400 * 7,
		HttpOnly: true,
	}
	sess.Values["loggedIn"] = true
	sess.Values["username"] = user.Username
	sess.Save(c.Request(), c.Response())

	return c.JSON(http.StatusOK, map[string]interface{}{
		"message": "success",
		"path":    "/myfiles",
	})
}

func uploadHandler(c echo.Context) error {

	title := c.FormValue("title")
	file, err := c.FormFile("file")
	if err != nil {
		return err
	}

	if len(title) < 1 || len(title) > 256 {
		return c.JSON(400, map[string]interface{}{
			"err":  "Something is Invalid",
			"path": "/?message=Title+Shouldn't+Empty+and+No+More+Than+256+Chars",
		})
	}

	wl_ext := []string{"jpg", "png", "bmp", "pdf", "txt"}
	f := strings.Split(file.Filename, ".")

	if len(f[0]) <= 0 {
		return c.JSON(400, map[string]interface{}{
			"err":  "Something is Invalid",
			"path": "/?message=Filename+is+invalid",
		})
	}

	if !slices.Contains(wl_ext, f[len(f)-1]) {
		return c.JSON(400, map[string]interface{}{
			"err":  "Something is Invalid",
			"path": "/?message=Extension+is+not+allowed",
		})
	}

	bl_ct := []string{"htm", "script", "octet-stream", "httpd", "svg", "xml"}
	ct := file.Header.Get("Content-Type")
	if slices.Contains(bl_ct, ct) {
		return c.JSON(400, map[string]interface{}{
			"err":  "Something is Invalid",
			"path": "/?message=File+is+not+allowed",
		})
	}
	src, err := file.Open()
	if err != nil {
		return err
	}

	defer src.Close()

	_uuid := uuid.Must(uuid.NewRandom()).String()
	if err := ensureDir("uploads/" + _uuid); err != nil {
		return err
	}

	dst, err := os.Create("uploads/" + _uuid + "/" + file.Filename)
	if err != nil {
		return err
	}
	defer dst.Close()

	if _, err = io.Copy(dst, src); err != nil {
		return err
	}

	sess, _ := session.Get("session", c)
	username, _ := sess.Values["username"].(string)
	fuplod := new(FilesUpload)
	fuplod.UUID = _uuid
	fuplod.Title = title
	fuplod.ContentType = file.Header.Get("Content-Type")
	fuplod.Filename = file.Filename
	fuplod.Username = username
	if err := saveFileToDB(fuplod); err != nil {
		return err
	}

	return c.Redirect(301, "/myfiles")
}

func viewFileHandler(c echo.Context) error {
	uuidp := c.Param("uuid")
	if !isValidUUID(uuidp) {
		return c.JSON(400, map[string]interface{}{
			"err":  "Something is Invalid",
			"path": "/?message=Invalid+UUID+Format",
		})
	}

	sess, _ := session.Get("session", c)
	fupload, err := getFile(uuidp, sess.Values["username"].(string))
	if err != nil {
		return err
	}
	c.Response().Header().Set("Content-Disposition", "attachment; filename=\""+sess.Values["username"].(string)+"-"+fupload.Filename+"\"")
	c.Response().Header().Set("Content-Security-Policy", "default-src 'none'; script-src 'none'; object-src 'none'; connect-src 'none'; navigate-to 'none'; base-uri 'none'; form-action 'none'; style-src 'none'; frame-src 'none'; sandbox")
	c.Response().Header().Set("Content-Type", fupload.ContentType)
	c.Response().Header().Set("X-Content-Type-Options", "nosniff")
	c.Response().Header().Set("X-Frame-Options", "DENY")
	c.Response().WriteHeader(http.StatusOK)

	return c.File(fmt.Sprintf("./uploads/%s/%s", fupload.UUID, fupload.Filename))
}

func getAllOwnedFilesHandler(c echo.Context) error {
	sess, _ := session.Get("session", c)
	fuploads, err := getOwnedFiles(sess.Values["username"].(string))
	if err != nil {
		return err
	}

	data := map[string]interface{}{
		"f":    fuploads,
		"csrf": c.Get(middleware.DefaultCSRFConfig.ContextKey).(string),
	}

	return c.Render(http.StatusOK, "myfiles.html", data)
}
