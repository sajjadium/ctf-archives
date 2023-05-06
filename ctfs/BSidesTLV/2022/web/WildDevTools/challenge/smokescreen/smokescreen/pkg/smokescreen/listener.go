package smokescreen

import (
	"net"
	"sync"

	"github.com/stripe/smokescreen/internal/einhorn"
)

// einhornListener is a net.Listener that will send an ACK to the einhorn
// master the first time its Accept method is called.
//
// Its implementation leaves a short time window between the sending the ACK
// and when a thread is actively blocked by an Accept syscall. Because there is
// a gap here it is possible for the process to freeze/crash/etc and never
// reach the Accept call. This may lead to sadness because of dropped
// connections (if the accept queue overflows) or timeouts because nothing
// realized this process died.
//
// The alternatives to work around this are complex, introduce concurrency and
// create several new classes of errors. So I've erred on the side of
// simplicity and am hoping that by moving the ACK as close to the Accept as
// possible we'll avoid too much pain.
type einhornListener struct {
	net.Listener

	firstAcceptOnce sync.Once

	accept func() (net.Conn, error)
}

func (el *einhornListener) firstAccept() (conn net.Conn, err error) {
	el.firstAcceptOnce.Do(func() {
		// Switch to the embedded Listener's Accept for all future calls
		el.accept = el.Listener.Accept

		// TODO: Should we just fire this into a goroutine so it will probably
		// happen after we start blocking on Accept and then log.Fatal if it
		// fails instead of returning an error?
		if err = einhorn.Ack(); err != nil {
			return
		}
	})
	if err != nil {
		return nil, err
	}

	return el.Accept()
}

func (el *einhornListener) Accept() (net.Conn, error) {
	if el.accept == nil {
		return el.firstAccept()
	}

	return el.accept()
}
