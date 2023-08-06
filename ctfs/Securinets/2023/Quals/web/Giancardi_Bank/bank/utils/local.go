package utils

import (
	"net/url"
)

func isLocal(urlStr string) (bool, error) {
	u, err := url.Parse(urlStr)
	if err != nil {
		return false, err
	}

	// Here, you can add the conditions as per your requirements.
	// localhost, 127.0.0.1, ::1 are commonly used for local addresses.
	switch u.Hostname() {
	case "", "localhost", "127.0.0.1", "::1":
		return true, nil
	default:
		return false, nil
	}
}
