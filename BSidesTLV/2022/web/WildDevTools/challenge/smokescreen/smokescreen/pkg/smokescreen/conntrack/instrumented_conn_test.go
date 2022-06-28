package conntrack

import (
	"fmt"
	"io"
	"log"
	"net"
	"testing"
	"time"

	"github.com/sirupsen/logrus"
	"github.com/stretchr/testify/assert"
)

// TestInstrumentedConnByteCounting sends a fixed size message between two
// instrumented connections and ensures the bytes in and out are correct.
func TestInstrumentedConnByteCounting(t *testing.T) {
	assert := assert.New(t)

	addr := "localhost:0"
	ln, err := net.Listen("tcp", addr)
	if err != nil {
		t.Fatal(err)
	}
	defer ln.Close()

	tr := NewTestTracker(0)
	sent := []byte("X-Smokescreen-Test")

	writerErrChan := make(chan error, 1)
	go func() {
		defer close(writerErrChan)
		conn, err := ln.Accept()
		if err != nil {
			writerErrChan <- fmt.Errorf("error accepting: %w", err)
			return
		}

		icWriter := tr.NewInstrumentedConn(conn, logrus.NewEntry(testLogger), "test", "localhost", "http")

		n, err := icWriter.Write(sent)
		if err != nil {
			writerErrChan <- fmt.Errorf("error writing: %w", err)
			return
		}
		conn.Close()

		if len(sent) != n {
			writerErrChan <- fmt.Errorf("length sent wasn't expected value: %d != %d", len(sent), n)
			return
		}
		bytesOut := *icWriter.BytesOut
		if uint64(len(sent)) != bytesOut {
			writerErrChan <- fmt.Errorf("bytes out value wasn't expected value: %d != %d", len(sent), bytesOut)
			return
		}
	}()

	conn, err := net.Dial("tcp", ln.Addr().String())
	if err != nil {
		t.Fatal(err)
	}
	icReader := tr.NewInstrumentedConn(conn, logrus.NewEntry(testLogger), "testBytesInOut", "localhost", "http")

	readerErrChan := make(chan error, 1)
	go func() {
		defer close(readerErrChan)
		read := make([]byte, len(sent))
		for {
			_, err := icReader.Read(read)
			if err != nil {
				if err != io.EOF {
					readerErrChan <- err
				}
				return
			}
			assert.Equal(sent, read)
		}
	}()

	assert.NoError(<-writerErrChan)
	assert.NoError(<-readerErrChan)
	assert.Equal(uint64(len(sent)), *icReader.BytesIn)
}

func TestInstrumentedConnIdle(t *testing.T) {
	assert := assert.New(t)

	tr := NewTestTracker(time.Millisecond)
	ic := tr.NewInstrumentedConn(&net.UnixConn{}, logrus.NewEntry(testLogger), "testIdle", "localhost", "egress")

	ic.Write([]byte("egress"))
	assert.False(ic.Idle())

	time.Sleep(time.Second)
	assert.True(ic.Idle())
}

var timeoutTests = []struct {
	name          string
	timeout       time.Duration
	expectedError bool
}{
	{"no timeout with zero duration", 0, false},
	{"timeout after duration", 50 * time.Millisecond, true},
}

func TestInstrumentedConnWithTimeout(t *testing.T) {
	addr := "localhost:0"
	ln, err := net.Listen("tcp", addr)
	if err != nil {
		t.Fatal(err)
	}
	defer ln.Close()

	handler := func(ln net.Listener, errCh chan error) {
		c, err := ln.Accept()
		errCh <- err
		time.Sleep(250 * time.Millisecond)
		c.Write([]byte("timeout-test"))
		defer c.Close()
	}

	tr := NewTestTracker(0)

	for _, tt := range timeoutTests {
		errCh := make(chan error)
		go handler(ln, errCh)

		c, err := net.Dial("tcp", ln.Addr().String())
		if err != nil {
			t.Fatal(err)
		}

		lnErr := <-errCh
		if lnErr != nil {
			t.Fatalf("failed to call Accept() on listener: %v", err)
		}

		var b [1]byte
		ic := tr.NewInstrumentedConnWithTimeout(c, tt.timeout, logrus.NewEntry(testLogger), "test", "testHost", "http")

		_, err = ic.Read(b[:])
		if err == nil && tt.expectedError {
			t.Fatalf("%v: expected=%v got=%v", tt.name, tt.expectedError, err)
		}

		if err != nil && !tt.expectedError {
			t.Fatalf("%v: expected=%v got=%v", tt.name, tt.expectedError, err)
		}

		if err != nil {
			if err, ok := err.(net.Error); ok && !err.Timeout() {
				log.Fatal(err)
				t.Fatalf("%v: expected timeout error - got: %v", tt.name, err)
			}
		}
		ic.Close()
	}
}
