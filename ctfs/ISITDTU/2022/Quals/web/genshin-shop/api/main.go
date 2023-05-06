package main

import (
	"log"
	"os"

	"github.com/ks75vl/genshin-shop-api/api"
	"github.com/ks75vl/genshin-shop-api/configs"
)

func main() {
	// Get config.
	defaultConfig, e := configs.Default()
	if e != nil {
		log.Printf("Can not load yaml config, e=%v\n", e)
		os.Exit(1)
		return
	}

	// Create api.
	a := api.New(defaultConfig)
	defer a.Release()

	// Setup.
	if ok := a.Setup(); !ok {
		os.Exit(1)
		return
	}

	// Run.
	if ok := a.Run(); !ok {
		os.Exit(1)
		return
	}
}
