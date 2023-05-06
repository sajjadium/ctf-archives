package main

/*
Just running BOT/chrome inside sandbox/container!
No bugs here.
*/

import (
	"bytes"
	"context"
	"errors"
	"github.com/docker/docker/api/types"
	"github.com/docker/docker/api/types/container"
	"github.com/docker/docker/api/types/network"
	"github.com/docker/docker/client"
	"io/ioutil"
	"os"
	"sync"
	"time"
)

var freeCore map[int]bool
var muFreeCore *sync.Mutex

func init() {
	maxCores := 0
	content, err := ioutil.ReadFile("/proc/cpuinfo")
	if err != nil {
		maxCores = 2 // just default
	} else {
		for _, line := range bytes.Split(content, []byte("\n")) {
			if bytes.Contains(line, []byte("processor")) {
				maxCores += 1
			}
		}
	}

	muFreeCore = &sync.Mutex{}
	freeCore = make(map[int]bool)
	for i := 1; i < maxCores; i++ {
		freeCore[i] = true
	}
}

func OpenCore() (int, error) {
	muFreeCore.Lock()
	defer muFreeCore.Unlock()
	for key, value := range freeCore {
		if value {
			freeCore[key] = false
			return key, nil
		}
	}
	return 0, errors.New("no free cpu")
}

func CloseCore(coreId int) {
	muFreeCore.Lock()
	defer muFreeCore.Unlock()
	freeCore[coreId] = true
}

func getMeContainerID() string {
	return os.Getenv("HOSTNAME")
}

func RunBot(url string) error {
	var err error
	coreIdx, err := OpenCore()
	if err != nil {
		return err
	}
	defer CloseCore(coreIdx)

	cli, err := client.NewClientWithOpts(client.FromEnv)
	if err != nil {
		return err
	}

	ctx, cancel := context.WithTimeout(context.Background(), time.Second*45)
	defer cancel()

	containerData, err := cli.ContainerInspect(ctx, getMeContainerID())
	if err != nil {
		return err
	}
	networkCfg := make(map[string]*network.EndpointSettings)
	for name, value := range containerData.NetworkSettings.Networks {
		value.IPAMConfig = nil
		value.Links = nil
		value.Aliases = nil
		value.IPAddress = ""
		networkCfg[name] = value
	}

	pkt, err := cli.ContainerCreate(
		ctx,
		&container.Config{
			Cmd:   []string{url},
			Image: os.Getenv("BOT_IMAGE"),
		},
		&container.HostConfig{
			AutoRemove: true,
			Resources: container.Resources{
				Memory: 1 * 1024 * 1024 * 1024, // 1GB
			},
		},
		&network.NetworkingConfig{
			EndpointsConfig: networkCfg,
		},
		nil,
		"",
	)
	if err != nil {
		return err
	}

	err = cli.ContainerStart(ctx, pkt.ID, types.ContainerStartOptions{})
	if err != nil {
		return err
	}

	resultC, errC := cli.ContainerWait(ctx, pkt.ID, container.WaitConditionRemoved)
	select {
	case err := <-errC:
		if err == context.DeadlineExceeded {
			cli.ContainerKill(context.Background(), pkt.ID, "9")
		}
		return err
	case result := <-resultC:
		if result.Error != nil {
			return errors.New(result.Error.Message)
		}
	}
	return nil
}
