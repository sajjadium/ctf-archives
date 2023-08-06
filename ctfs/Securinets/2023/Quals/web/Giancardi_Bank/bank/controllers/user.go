package controllers

import (
	"fmt"
	"go-get-it/config"
	"go-get-it/middlewares"
	"go-get-it/models"
	"go-get-it/sessions"
	"net/http"
	"path/filepath"
	"strconv"
	"strings"
	"time"

	"github.com/gofiber/fiber/v2"
)

func RegisterUserHandler(app *fiber.App) {

	userGroup := app.Group("/user", middlewares.IsAuthenticated)
	app.Get("/verify/:id", middlewares.IsLocal, ViewUserProfile)
	userGroup.Get("/", ViewProfile)
	userGroup.Get("/password-change", ViewPasswordChange)
	userGroup.Post("/password-change", PostPasswordChange)
	userGroup.Get("/pet-files", ViewPetFiles)
	userGroup.Get("/pet-files/:id", ViewPetFile)
	userGroup.Post("/pet-files", PostPetFile)
	userGroup.Get("/financial-note", ViewFinancialNotes)
	userGroup.Get("/financial-note/new", ViewFinancialNoteForm)
	userGroup.Post("/financial-note/new", PostFinancialNoteForm)
	userGroup.Get("/financial-note/:id/edit", ViewFinancialNoteEditForm)
	userGroup.Post("/financial-note/:id/edit", UpdateFinancialNote)
	app.Get("/financial-note/view/:title", middlewares.IsLocal, ViewFinancialNote)

}

func ViewProfile(c *fiber.Ctx) error {
	s, err := sessions.RSS.Get(c)

	if err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	userId, ok := s.Get("user_id").(uint)

	if !ok {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	var user models.User
	if err := models.GetUserById(&user, userId).Error; err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	return c.Render("profile", user)
}

func ViewUserProfile(c *fiber.Ctx) error {

	id, err := c.ParamsInt("id")

	if err != nil {
		return c.Status(http.StatusBadRequest).SendString("Invalid ID")
	}

	uid := uint(id)

	var user models.User
	if err := models.GetUserById(&user, uid).Error; err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}
	return c.SendStatus(200)
}

func ViewPasswordChange(c *fiber.Ctx) error {
	return c.Render("password_change", nil)
}

func PostPasswordChange(c *fiber.Ctx) error {
	newPass := c.FormValue("new_password")
	confirmNewPass := c.FormValue("confirm_new_password")
	oldPass := c.FormValue("old_password")

	if newPass != confirmNewPass {
		c.SendString("Passwords do not match")
		return c.Status(http.StatusBadRequest).SendString("Passwords do not match")
	}

	if len(newPass) < 8 {
		c.SendString("Password must be at least 8 characters")
		return c.Status(http.StatusBadRequest).SendString("Password must be at least 8 characters")
	}

	s, err := sessions.RSS.Get(c)
	if err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	userId, ok := s.Get("user_id").(uint)

	if !ok {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	var user models.User
	if err := models.GetUserById(&user, userId).Error; err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Error finding user")
	}

	if err := user.CheckPassword(oldPass); !err {
		return c.Status(http.StatusBadRequest).SendString("Make sure you have entered the correct passwor")
	}

	if err := user.UpdatePassword(newPass); err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error: Error updating password")
	}

	return c.Redirect("/profile")
}

func ViewFinancialNote(c *fiber.Ctx) error {
	title := c.Params("title")

	var financialNote models.FinanceNote

	if len(title) < 4 {
		return c.Status(http.StatusBadRequest).SendString("Note must be at least 4 character and same for its title.")
	}

	res, err := config.Cache.Get(title)

	if err != nil && res != "" {
		financialNote.Title = title
		financialNote.Note = res
		return c.Render("financial_note", financialNote)
	}

	s, err := sessions.RSS.Get(c)

	if err != nil {
		fmt.Println(err)
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	userId, ok := s.Get("user_id").(uint)

	if !ok {
		fmt.Println(err,userId)
	}

	if err := models.GetUserNoteByTitle(&financialNote, title); err != nil {
		return c.SendStatus(http.StatusNotFound)
	}

	if err := config.Cache.Set(title, financialNote.Note); err != nil {
		fmt.Println(err)
		return c.SendStatus(http.StatusInternalServerError)
	}

	return c.Render("financial_note", financialNote)

}

func PostPetFile(c *fiber.Ctx) error {

	file, err := c.FormFile("file")

	if err != nil {
		return err
	}

	if file.Size > 1024*1024*5 {
		return c.Status(http.StatusBadRequest).SendString("File too large")
	}

	if !strings.HasPrefix(file.Header["Content-Type"][0], "image/") {
		return c.Status(http.StatusBadRequest).SendString("File must be an image")
	}

	ext := filepath.Ext(file.Filename)

	if ext != ".jpg" && ext != ".png" && ext != ".jpeg" {
		return c.Status(http.StatusBadRequest).SendString("File must be an image")
	}

	filename := fmt.Sprintf("%d%s", time.Now().UnixNano(), ext)

	if err := c.SaveFile(file, filename); err != nil {
		return err
	}

	s, err := sessions.RSS.Get(c)

	if err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	currentUser, ok := s.Get("user_id").(uint)
	if !ok {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	var user models.User
	if err := models.GetUserById(&user, currentUser).Error; err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	petFile := models.PetFile{
		Path:   filename,
		UserID: user.ID,
	}

	if err := models.CreatePetFile(&petFile); err != nil {
		return err
	}

	return c.Redirect("/pet-files")

}

func ViewPetFiles(c *fiber.Ctx) error {
	var petFiles []models.PetFile

	s, err := sessions.RSS.Get(c)

	if err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	userId, ok := s.Get("user_id").(uint)
	if !ok {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	if err := models.GetUserPetFiles(&petFiles, userId); err != nil {
		return c.SendStatus(http.StatusNotFound)
	}

	return c.Render("pet_files", petFiles)
}

func ViewPetFile(c *fiber.Ctx) error {
	id, err := c.ParamsInt("id")
	if err != nil {
		return c.Status(http.StatusBadRequest).SendString("Invalid ID")
	}

	uid := uint(id)
	var petFile models.PetFile

	s, err := sessions.RSS.Get(c)

	if err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	userId, ok := s.Get("user_id").(uint)
	if !ok {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	if err := models.GetUserPetFile(&petFile, uid, userId).Error; err != nil {
		return c.SendStatus(http.StatusNotFound)
	}

	return c.Render("pet_file", petFile)
}

func ViewFinancialNotes(c *fiber.Ctx) error {
	var financialNotes []models.FinanceNote

	s, err := sessions.RSS.Get(c)

	if err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	userId, ok := s.Get("user_id").(uint)

	if !ok {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	if err := models.GetUserFinanceNotes(&financialNotes, userId); err != nil {
		return err
	}

	return c.Render("financial_notes", financialNotes)
}

func ViewFinancialNoteForm(c *fiber.Ctx) error {
	return c.Render("financial_note_form", nil)
}

func PostFinancialNoteForm(c *fiber.Ctx) error {
	note := c.FormValue("note")
	title := c.FormValue("title")

	if len(note) < 1 || len(title) < 1 {
		return c.Status(http.StatusBadRequest).SendString("Note must be at least 1 character and same for its title.")
	}

	s, err := sessions.RSS.Get(c)

	if err != nil {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	userId, ok := s.Get("user_id").(uint)

	if !ok {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	financialNote := models.FinanceNote{
		Note:   note,
		UserID: userId,
		Title:  title,
	}

	if err := models.CreateFinanceNote(&financialNote); err != nil {
		return err
	}

	return c.Redirect("/user/financial-note")
}

func ViewFinancialNoteEditForm(c *fiber.Ctx) error {
	id, err := strconv.Atoi(c.Params("id"))
	if err != nil {
		return c.Status(http.StatusBadRequest).SendString("Invalid ID")
	}

	uid := uint(id)

	s, _ := sessions.RSS.Get(c)
	userId, ok := s.Get("user_id").(uint)
	if !ok {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	var financialNote models.FinanceNote
	if err := models.GetUserNoteById(&financialNote, uid, userId); err != nil {
		return c.SendStatus(http.StatusNotFound)
	}

	return c.Render("financial_note_edit_form", financialNote)
}

func UpdateFinancialNote(c *fiber.Ctx) error {
	n := c.FormValue("note")
	t := c.FormValue("title")

	if len(n) < 1 || len(t) < 1 {
		return c.Status(http.StatusBadRequest).SendString("Note must be at least 1 character and same for its title.")
	}

	id, err := strconv.Atoi(c.Params("id"))
	if err != nil {
		return c.Status(http.StatusBadRequest).SendString("Invalid ID")
	}

	uid := uint(id)

	s, err := sessions.RSS.Get(c)

	if err != nil {
		return c.SendStatus(http.StatusInternalServerError)
	}

	userId, ok := s.Get("user_id").(uint)
	if !ok {
		return c.Status(http.StatusInternalServerError).SendString("Internal Server Error")
	}

	var financialNote models.FinanceNote
	if err := models.GetUserNoteById(&financialNote, uid, userId); err != nil {
		return c.SendStatus(http.StatusNotFound)
	}

	financialNote.Note = n
	financialNote.Title = t
	models.UpdateFinanceNote(&financialNote)

	return c.Redirect("/user/financial-note")
}
