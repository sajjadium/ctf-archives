package main

import (
	"encoding/json"
	"fmt"
	"os"
	"sort"
	"strings"

	"github.com/gin-contrib/sessions"
	"github.com/samber/lo"
)

type User struct {
	ID    string
	Query string
}

type Note struct {
	ID      string
	Content string `form:"content" binding:"required"`
}

func createUser() (*User, error) {
	user := new(User)
	user.ID = getRandomHex(12)
	if err := os.Mkdir(fmt.Sprintf("notes/%s", user.ID), 0700); err != nil {
		return nil, err
	}
	return user, nil
}

func getUser(sess sessions.Session) (*User, error) {
	data, ok := sess.Get("user").([]byte)
	if !ok {
		return createUser()
	}
	user := new(User)
	if err := json.Unmarshal(data, user); err != nil {
		return nil, err
	}
	return user, nil
}

func (user *User) save(sess sessions.Session) error {
	data, err := json.Marshal(user)
	if err != nil {
		return err
	}
	sess.Set("user", data)
	return sess.Save()
}

func (user *User) getNotes(query string) ([]Note, error) {
	files, err := os.ReadDir(fmt.Sprintf("notes/%s", user.ID))
	if err != nil {
		return nil, err
	}
	notes := make([]Note, 0, len(files))
	for _, file := range files {
		content, err := os.ReadFile(fmt.Sprintf("notes/%s/%s", user.ID, file.Name()))
		if err != nil {
			return nil, err
		}
		notes = append(notes, Note{
			ID:      file.Name(),
			Content: string(content),
		})
	}
	notes = lo.Filter(notes, func(note Note, _ int) bool {
		return strings.Contains(note.Content, query)
	})
	sort.Slice(notes, func(i, j int) bool {
		return notes[i].Content < notes[j].Content
	})
	return notes, nil
}

func (user *User) createNote(note *Note) error {
	note.ID = getRandomHex(12)
	return os.WriteFile(fmt.Sprintf("notes/%s/%s", user.ID, note.ID), []byte(note.Content), 0600)
}

func (user *User) deleteNote(noteID string) error {
	return os.Remove(fmt.Sprintf("notes/%s/%s", user.ID, noteID))
}
