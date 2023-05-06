// GENERATED CODE - DO NOT EDIT
// This file is the main file for Revel.
// It registers all the controllers and provides details for the Revel server engine to
// properly inject parameters directly into the action endpoints.
package main

import (
	"flag"
	"horoscope/app/tmp/run"
	"github.com/revel/revel"
)

var (
	runMode    *string = flag.String("runMode", "", "Run mode.")
	port       *int    = flag.Int("port", 0, "By default, read from app.conf")
	importPath *string = flag.String("importPath", "", "Go Import Path for the app.")
	srcPath    *string = flag.String("srcPath", "", "Path to the source root.")

)

func main() {
	flag.Parse()
	revel.Init(*runMode, *importPath, *srcPath)
	run.Run(*port)
}
