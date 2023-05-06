package main

import (
	"fmt"
	"github.com/tebeka/selenium"
	"github.com/tebeka/selenium/chrome"
	"net"
	"os"
	"os/exec"
	"time"
)

func FindBinaryPath(binary string) string {
	path, err := exec.LookPath(binary)
	if err != nil {
		return binary
	}
	return path
}

func GetFreePort() (int, error) {
	addr, err := net.ResolveTCPAddr("tcp", "localhost:0")
	if err != nil {
		return 0, err
	}

	l, err := net.ListenTCP("tcp", addr)
	if err != nil {
		return 0, err
	}
	defer l.Close()
	return l.Addr().(*net.TCPAddr).Port, nil
}

type browser struct {
	port    int
	service *selenium.Service
}

func NewBrowser() (*browser, error) {
	freePort, err := GetFreePort()
	if err != nil {
		return nil, err
	}
	opts := []selenium.ServiceOption{
		selenium.Output(os.Stderr),
	}
	service, err := selenium.NewChromeDriverService(FindBinaryPath("chromedriver"), freePort, opts...)
	if err != nil {
		return nil, err
	}

	s := &browser{
		service: service,
		port:    freePort,
	}
	return s, nil
}

func (b *browser) Get(url string) error {
	caps := selenium.Capabilities{
		"browserName": "chrome",
	}
	caps.AddChrome(chrome.Capabilities{
		Path: FindBinaryPath("google-chrome-stable"),
		Args: []string{
			"--no-sandbox",
			"--headless",
			"--window-size=1420,1080",
			"--disable-gpu",
			"--disable-dev-shm-usage",
		},
	})
	browser, err := selenium.NewRemote(caps, fmt.Sprintf("http://localhost:%d/wd/hub", b.port))
	if err != nil {
		return err
	}
	defer browser.Quit()

	err = browser.SetPageLoadTimeout(time.Second * 30)
	if err != nil {
		return err
	}

	err = browser.Get(url)
	if err != nil {
		return err
	}
	return nil
}

func (b *browser) Close() error {
	return b.service.Stop()
}

func main() {
	go func() {
		// hard timeout just in case
		time.Sleep(time.Second * 35)
		os.Exit(1)
	}()

	url := os.Args[1]
	b, err := NewBrowser()
	if err != nil {
		panic(err)
	}
	defer b.Close()

	err = b.Get(url)
	if err != nil {
		panic(err)
	}
}
