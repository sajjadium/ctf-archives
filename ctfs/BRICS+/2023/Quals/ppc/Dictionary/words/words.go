package words

import (
	_ "embed"
	"strings"
)

//go:embed words.txt
var file string

// List returns words as a list of strings.
// This is a function to avoid loading words when not needed.
func List() []string {
	lines := strings.Split(file, "\n")
	return lines[:len(lines)-1]
}
