package conntrack

import (
	"sync"
	"sync/atomic"
	"time"

	"github.com/DataDog/datadog-go/statsd"
	"github.com/sirupsen/logrus"
)

type Tracker struct {
	*sync.Map
	ShuttingDown atomic.Value
	Wg           *sync.WaitGroup
	statsc       statsd.ClientInterface

	// A connection is idle if it has been inactive (no bytes in/out) for this
	// many seconds.
	IdleTimeout time.Duration
}

func NewTracker(idle time.Duration, statsc statsd.ClientInterface, logger *logrus.Logger, sd atomic.Value) *Tracker {
	return &Tracker{
		Map:          &sync.Map{},
		ShuttingDown: sd,
		Wg:           &sync.WaitGroup{},
		IdleTimeout:  idle,
		statsc:       statsc,
	}
}

// MaybeIdleIn returns the longest amount of time it will take for all tracked
// connections to become idle based on the configured IdleTimeout.
//
// A duration of 0 indicates all connections are idle.
func (tr *Tracker) MaybeIdleIn(d time.Duration) time.Duration {
	longest := 0 * time.Nanosecond
	tr.Range(func(k, v interface{}) bool {
		c := k.(*InstrumentedConn)

		lastActivity := time.Unix(0, atomic.LoadInt64(c.LastActivity))
		idleAt := lastActivity.Add(d)
		idleIn := time.Until(idleAt)

		if idleIn > longest {
			longest = idleIn
		}
		return true
	})
	return longest
}
