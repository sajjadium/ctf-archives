package einhorn

import (
	"errors"
	"fmt"
	"net"
	"os"
	"strconv"
)

// CountListeners returns the number of listener fd's passed by the master.
func CountListeners() int {
	count, err := strconv.Atoi(os.Getenv("EINHORN_FD_COUNT"))
	if err != nil {
		return 0
	}
	return count
}

// GetListener returns the passed listener with the specified index.
func GetListener(index int) (net.Listener, error) {
	if CountListeners() < (index + 1) {
		return nil, errors.New("einhorn: too few EINHORN_FDs passed")
	}

	name := fmt.Sprintf("EINHORN_FD_%d", index)

	fileno, err := strconv.Atoi(os.Getenv(name))
	if err != nil {
		return nil, err
	}

	listener, err := net.FileListener(os.NewFile(uintptr(fileno), name))
	if err != nil {
		return nil, err
	}

	return listener, nil
}

// IsWorker returns whether the current process is an einhorn worker.
func IsWorker() bool {
	masterPid := os.Getenv("EINHORN_MASTER_PID")
	if masterPid == "" {
		return false
	}

	pid, err := strconv.Atoi(masterPid)
	if err != nil {
		return false
	}

	return pid == os.Getppid()
}

// Ack sends an ack to the einhorn master.
func Ack() error {
	client, err := NewClientForPath(os.Getenv("EINHORN_SOCK_PATH"))
	if err != nil {
		return err
	}

	defer client.Close()

	return client.SendRequest(&ClientAckRequest{
		Command: "worker:ack",
		Pid:     os.Getpid(),
	})
}
