package conntrack

import "time"

type InstrumentedConnStats struct {
	Role                     string    `json:"role"`
	Rhost                    string    `json:"rhost"`
	Raddr                    string    `json:"raddr"`
	Created                  time.Time `json:"created"`
	BytesIn                  uint64    `json:"bytesIn"`
	BytesOut                 uint64    `json:"bytesOut"`
	SecondsSinceLastActivity float64   `json:"secondsSinceLastActivity"`
	ProxyType                string    `json:"proxyType"`
}
