package utils

import (
	"crypto/sha256"
	"encoding/hex"

	"golang.org/x/crypto/bcrypt"
)

func HashPassword(password string) (string, error) {
	bytes, err := bcrypt.GenerateFromPassword([]byte(password), 14)
	return string(bytes), err
}

func CheckPasswordHash(password, hash string) bool {
	err := bcrypt.CompareHashAndPassword([]byte(hash), []byte(password))
	return err == nil
}

func HashStringToSha256(s string) string {

	h := sha256.New()
	h.Write([]byte(s))

	hashed := h.Sum(nil)

	res := hex.EncodeToString(hashed)

	return res
}
