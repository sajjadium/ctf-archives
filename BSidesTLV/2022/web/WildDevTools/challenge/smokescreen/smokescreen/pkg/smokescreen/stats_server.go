package smokescreen

import (
	"fmt"
	"net"
	"net/http"
	"os"

	"github.com/stripe/smokescreen/pkg/smokescreen/conntrack"
)

type StatsServer struct {
	config     *Config
	ln         net.Listener
	mux        *http.ServeMux
	socketPath string
}

func newServer(config *Config) (s *StatsServer) {
	s = &StatsServer{
		config: config,
		mux:    http.NewServeMux(),
	}

	s.mux.HandleFunc("/", s.stats)
	return
}

func (s *StatsServer) Serve() {
	pid := os.Getpid()
	s.socketPath = fmt.Sprintf("%s/track-%d.sock", s.config.StatsSocketDir, pid)
	ln, err := net.Listen("unix", s.socketPath)

	if err != nil {
		s.config.Log.Fatal("Could not start the reporting server: ", err)
	}
	os.Chmod(s.socketPath, s.config.StatsSocketFileMode)

	s.ln = ln
	err = http.Serve(s.ln, s.mux)
	if err != nil {
		s.config.Log.Fatal("Could not start the reporting server: ", err)
	}
}

func (s *StatsServer) Shutdown() {
	s.ln.Close()
	os.Remove(s.socketPath)
}

func (s *StatsServer) ServeHTTP(w http.ResponseWriter, req *http.Request) {
	s.mux.ServeHTTP(w, req)
}

func (s *StatsServer) stats(rw http.ResponseWriter, req *http.Request) {
	rw.Header().Set("Content-Type", "application/json")
	rw.Write([]byte{
		byte('['),
		byte('\n'),
	})

	firstRun := true

	s.config.ConnTracker.Range(func(k, v interface{}) bool {
		if !firstRun {
			rw.Write([]byte{byte(','), byte('\n')})
		}
		firstRun = false
		instrumentedConn := k.(*conntrack.InstrumentedConn)
		repr, err := instrumentedConn.JsonStats()

		if err != nil {
			s.config.Log.Error(err)
		}

		rw.Write(repr)
		return true
	})

	rw.Write([]byte{
		byte(']'),
		byte('\n'),
	})
}

func StartStatsServer(config *Config) *StatsServer {
	server := newServer(config)
	go server.Serve()
	return server
}
