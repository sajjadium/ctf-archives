package main

import (
	"database/sql"
	"fmt"

	_ "github.com/mattn/go-sqlite3"
)

var db *sql.DB

func init() {
	var err error
	// db, err = sql.Open("sqlite3", "file::memory:?cache=shared")
	db, err = sql.Open("sqlite3", "./stargazer.db")
	if err != nil {
		panic(err)
	}
	if err = db.Ping(); err != nil {
		panic(err)
	}
	createTable()
}

func createTable() {
	var schema = `
	CREATE TABLE IF NOT EXISTS users (
		id 			INTEGER PRIMARY KEY AUTOINCREMENT,
		username 	TEXT NOT NULL,
		password	TEXT NOT NULL
	);

	CREATE TABLE IF NOT EXISTS files (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		uuid 			TEXT NOT NULL,
		title 			TEXT NOT NULL,
		content_type	TEXT NOT NULL,
		filename		TEXT NOT NULL,
		username 		TEXT NOT NULL
	);
	`
	_, err := db.Exec(schema)

	if err != nil {
		panic(err)
	}
}

func loginUser(user *User) (int, error) {
	var count int
	stmt, err := db.Prepare("SELECT COUNT(*) FROM users WHERE username = ? AND password = ?")
	if err != nil {
		return 0, err
	}
	defer stmt.Close()

	err = stmt.QueryRow(user.Username, user.Password).Scan(&count)
	if err != nil {
		if err == sql.ErrNoRows {
			return 0, err
		}
		return 0, err
	}

	if count == 1 {
		return 1, err
	}

	return 0, err
}

func registerUser(username string, password string) error {
	var count int
	err := db.QueryRow("SELECT COUNT(*) FROM users WHERE username = ?", username).Scan(&count)
	if err != nil {
		return err
	}
	if count > 0 {
		return fmt.Errorf("username is already taken")
	}

	stmt, err := db.Prepare("INSERT INTO users (username, password) VALUES (?, ?)")
	if err != nil {
		return err
	}
	defer stmt.Close()

	_, err = stmt.Exec(username, password)
	if err != nil {
		return err
	}

	return err
}

func saveFileToDB(fupload *FilesUpload) error {
	stmt, err := db.Prepare("INSERT INTO files (uuid, title, content_type, filename, username) VALUES (?, ?, ?, ?, ?)")
	if err != nil {
		return err
	}
	defer stmt.Close()

	_, err = stmt.Exec(fupload.UUID, fupload.Title, fupload.ContentType, fupload.Filename, fupload.Username)
	if err != nil {
		return err
	}

	return err
}

func getOwnedFiles(username string) ([]*FilesUpload, error) {
	fuploads := []*FilesUpload{}
	rows, err := db.Query("SELECT uuid, title, content_type, filename, username FROM files WHERE username = ?", username)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	for rows.Next() {
		fupload := &FilesUpload{}
		err := rows.Scan(&fupload.UUID, &fupload.Title, &fupload.ContentType, &fupload.Filename, &fupload.Username)
		if err != nil {
			return nil, err
		}
		fuploads = append(fuploads, fupload)
	}
	if err = rows.Err(); err != nil {
		return nil, err
	}
	return fuploads, nil
}

func getFile(_uuid string, username string) (*FilesUpload, error) {
	fupload := &FilesUpload{}
	err := db.QueryRow("SELECT uuid, title, content_type, filename, username FROM files WHERE uuid = ? AND username = ?", _uuid, username).Scan(&fupload.UUID, &fupload.Title, &fupload.ContentType, &fupload.Filename, &fupload.Username)
	if err != nil {
		return nil, err
	}
	return fupload, nil
}
