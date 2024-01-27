package main

import (
	"flag"
	"os/exec"

	"github.com/songgao/water"
)

var platformSpecificParams water.PlatformSpecificParams

func init() {
	flag.StringVar(&platformSpecificParams.Name, "ifname", "tap0", "Linux - tap interface name")
	flag.BoolVar(&platformSpecificParams.Persist, "persist", false, "Linux - tap interface persist")
}

// ensure interface up
func tapFixup() {
	_ = exec.Command("/usr/sbin/ip", "link", "set", platformSpecificParams.Name, "up").Run()
}
