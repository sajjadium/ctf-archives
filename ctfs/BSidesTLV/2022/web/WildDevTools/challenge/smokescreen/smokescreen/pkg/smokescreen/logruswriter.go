// From https://github.com/sirupsen/logrus/issues/436
package smokescreen

import (
	"github.com/sirupsen/logrus"
)

type Log2LogrusWriter struct {
	Entry *logrus.Entry
}

func (w *Log2LogrusWriter) Write(b []byte) (int, error) {
	n := len(b)
	if n > 0 && b[n-1] == '\n' {
		b = b[:n-1]
	}
	w.Entry.Warning(string(b))
	return n, nil
}
