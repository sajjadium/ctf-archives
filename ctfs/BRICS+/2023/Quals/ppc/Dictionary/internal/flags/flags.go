package flags

import (
	"strings"

	"gitlab.com/NebulousLabs/fastrand"
)

const alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"

// Split splits a flag into len(flag) strings each of random length from min to max,
// where i'th string ends on flag[i].
func Split(flag string, min, max int) []string {
	parts := make([]string, len(flag))

	for i, letter := range flag {
		n := fastrand.Intn(max-min+1) + min

		var sb strings.Builder
		sb.Grow(n)

		for i := 0; i < n-1; i++ {
			sb.WriteByte(alphabet[fastrand.Intn(len(alphabet))])
		}

		sb.WriteRune(letter)
		parts[i] = sb.String()
	}

	return parts
}
