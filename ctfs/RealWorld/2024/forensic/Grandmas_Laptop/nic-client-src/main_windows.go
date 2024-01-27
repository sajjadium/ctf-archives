package main

import (
	"flag"

	"github.com/songgao/water"
)

var platformSpecificParams water.PlatformSpecificParams

func init() {
	flag.StringVar(&platformSpecificParams.ComponentID, "ComponentId", `root\tap0901`, "Windows - ComponentId")
	flag.StringVar(&platformSpecificParams.InterfaceName, "InterfaceName", "OpenVPN TAP-Windows6", "Windows - InterfaceName")
}

func tapFixup() {
}
