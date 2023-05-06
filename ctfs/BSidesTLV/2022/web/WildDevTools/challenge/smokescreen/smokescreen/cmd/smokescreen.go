package cmd

import (
	"errors"
	"fmt"
	"math"
	"os"
	"strconv"
	"time"

	log "github.com/sirupsen/logrus"
	"gopkg.in/urfave/cli.v1"

	"github.com/stripe/smokescreen/pkg/smokescreen"
	"github.com/stripe/smokescreen/pkg/smokescreen/conntrack"
)

// Process command line args into a configuration object.  If the "--help" or
// "--version" flags are provided, return nil with no error.
// If args is nil, os.Args will be used.  If logger is nil, a default logger
// will be created and included in the returned configuration.
func NewConfiguration(args []string, logger *log.Logger) (*smokescreen.Config, error) {
	if args == nil {
		args = os.Args
	}

	var configToReturn *smokescreen.Config

	app := cli.NewApp()
	app.Name = "smokescreen"
	app.Version = smokescreen.Version()
	app.Usage = "A simple HTTP proxy that prevents SSRF and can restrict destinations"
	app.ArgsUsage = " " // blank but non-empty to suppress default "[arguments...]"

	// Suppress "help" subcommand, as we have no other subcommands.
	// Unfortunately, this also suppresses "--help", so we'll add it back in
	// manually below.  See https://github.com/urfave/cli/issues/523
	app.HideHelp = true

	app.Flags = []cli.Flag{
		cli.BoolFlag{
			Name:  "help",
			Usage: "Show this help text.",
		},
		cli.StringFlag{
			Name:  "config-file",
			Usage: "Load configuration from `FILE`.  Command line options override values in the file.",
		},
		cli.StringFlag{
			Name:  "listen-ip",
			Usage: "Listen on interface with address `IP`.\n\t\tThis argument is ignored when running under Einhorn. (default: any)",
		},
		cli.UintFlag{
			Name:  "listen-port",
			Value: 4750,
			Usage: "Listen on port `PORT`.\n\t\tThis argument is ignored when running under Einhorn.",
		},
		cli.DurationFlag{
			Name:  "timeout",
			Value: time.Duration(10) * time.Second,
			Usage: "Time out after `DURATION` when connecting.",
		},
		cli.BoolFlag{
			Name:  "proxy-protocol",
			Usage: "Enable PROXY protocol support.",
		},
		cli.StringSliceFlag{
			Name:  "deny-range",
			Usage: "Add `RANGE`(in CIDR notation) to list of blocked IP ranges.  Repeatable.",
		},
		cli.StringSliceFlag{
			Name:  "allow-range",
			Usage: "Add `RANGE` (in CIDR notation) to list of allowed IP ranges.  Repeatable.",
		},
		cli.StringSliceFlag{
			Name:  "deny-address",
			Usage: "Add IP[:PORT] to list of blocked IPs.  Repeatable.",
		},
		cli.StringSliceFlag{
			Name:  "allow-address",
			Usage: "Add IP[:PORT] to list of allowed IPs.  Repeatable.",
		},
		cli.StringFlag{
			Name:  "egress-acl-file",
			Usage: "Validate egress traffic against `FILE`",
		},
		cli.StringSliceFlag{
			Name:  "resolver-address",
			Usage: "Make DNS requests to `ADDRESS` (IP:port).  Repeatable.",
		},
		cli.StringFlag{
			Name:  "statsd-address",
			Value: "127.0.0.1:8200",
			Usage: "Send metrics to statsd at `ADDRESS` (IP:port).",
		},
		cli.StringFlag{
			Name:  "tls-server-bundle-file",
			Usage: "Authenticate to clients using key and certs from `FILE`",
		},
		cli.StringSliceFlag{
			Name:  "tls-client-ca-file",
			Usage: "Validate client certificates using Certificate Authority from `FILE`",
		},
		cli.StringSliceFlag{
			Name:  "tls-crl-file",
			Usage: "Verify validity of client certificates against Certificate Revocation List from `FILE`",
		},
		cli.StringFlag{
			Name:  "additional-error-message-on-deny",
			Usage: "Display `MESSAGE` in the HTTP response if proxying request is denied",
		},
		cli.StringSliceFlag{
			Name:  "disable-acl-policy-action",
			Usage: "Disable usage of a `POLICY ACTION` such as \"open\" in the egress ACL",
		},
		cli.StringFlag{
			Name:  "stats-socket-dir",
			Usage: "Enable connection tracking. Will expose one UDS in `DIR` going by the name of \"track-{pid}.sock\".\n\t\tThis should be an absolute path with all symlinks, if any, resolved.",
		},
		cli.StringFlag{
			Name:  "stats-socket-file-mode",
			Value: "700",
			Usage: "Set the filemode to `FILE_MODE` on the statistics socket",
		},
		cli.BoolFlag{
			Name:  "unsafe-allow-private-ranges",
			Usage: "Allow private ip ranges by default",
		},
	}

	app.Action = func(c *cli.Context) error {
		if c.Bool("help") {
			cli.ShowAppHelp(c)
			return nil // configToReturn will not be set
		}
		if len(c.Args()) > 0 {
			return errors.New("Received unexpected non-option argument(s)")
		}

		var conf *smokescreen.Config
		if file := c.String("config-file"); file != "" {
			var err error
			conf, err = smokescreen.LoadConfig(file)
			if err != nil {
				return fmt.Errorf("Couldn't load file \"%s\" specified by --config-file: %v", file, err)
			}
		} else {
			conf = smokescreen.NewConfig()
		}

		if logger != nil {
			conf.Log = logger
		}

		if c.IsSet("listen-ip") {
			conf.Ip = c.String("listen-ip")
		}

		if c.IsSet("listen-port") {
			port := c.Uint("listen-port")
			if port > math.MaxUint16 {
				return fmt.Errorf("Invalid listen-port: %d", port)
			}
			conf.Port = uint16(port)
		}

		if c.IsSet("timeout") {
			conf.ConnectTimeout = c.Duration("timeout")
		}

		if c.IsSet("proxy-protocol") {
			conf.SupportProxyProtocol = c.Bool("proxy-protocol")
		}

		if c.IsSet("additional-error-message-on-deny") {
			conf.AdditionalErrorMessageOnDeny = c.String("additional-error-message-on-deny")
		}

		if c.IsSet("disable-acl-policy-action") {
			conf.DisabledAclPolicyActions = c.StringSlice("disable-acl-policy-action")
		}

		if c.IsSet("stats-socket-dir") {
			conf.StatsSocketDir = c.String("stats-socket-dir")
		}

		if c.IsSet("stats-socket-file-mode") {
			filemode, err := strconv.ParseInt(c.String("stats-socket-file-mode"), 8, 9)
			if err != nil {
				return err
			}
			conf.StatsSocketFileMode = os.FileMode(filemode)
		}

		if c.IsSet("deny-range") {
			if err := conf.SetDenyRanges(c.StringSlice("deny-range")); err != nil {
				return err
			}
		}

		if c.IsSet("allow-range") {
			if err := conf.SetAllowRanges(c.StringSlice("allow-range")); err != nil {
				return err
			}
		}

		if c.IsSet("deny-address") {
			if err := conf.SetDenyAddresses(c.StringSlice("deny-address")); err != nil {
				return err
			}
		}

		if c.IsSet("resolver-address") {
			if err := conf.SetResolverAddresses(c.StringSlice("resolver-address")); err != nil {
				return err
			}
		}

		if c.IsSet("allow-address") {
			if err := conf.SetAllowAddresses(c.StringSlice("allow-address")); err != nil {
				return err
			}
		}

		if c.IsSet("statsd-address") {
			if err := conf.SetupStatsd(c.String("statsd-address")); err != nil {
				return err
			}
		}

		if c.IsSet("egress-acl-file") {
			if err := conf.SetupEgressAcl(c.String("egress-acl-file")); err != nil {
				return err
			}
		}

		if c.IsSet("tls-crl-file") {
			if err := conf.SetupCrls(c.StringSlice("tls-crl-file")); err != nil {
				return err
			}
		}

		if c.IsSet("unsafe-allow-private-ranges") {
			conf.UnsafeAllowPrivateRanges = c.Bool("unsafe-allow-private-ranges")
		}

		// FIXME: mixing and matching parts of TLS config between cli and file
		// hasn't been thought through and likely won't work

		if c.IsSet("tls-server-bundle-file") {
			// Originally, we assumed a single file with both cert and key
			// concatenated.  That setup will continue to work, but SetupTLS now
			// takes separate args for cert and key, so we pass the filename twice
			// here.
			bundleFile := c.String("tls-server-bundle-file")
			if err := conf.SetupTls(
				bundleFile,
				bundleFile,
				c.StringSlice("tls-client-ca-file")); err != nil {
				return err
			}
		}

		// Setup the connection tracker
		conf.ConnTracker = conntrack.NewTracker(conf.IdleTimeout, conf.MetricsClient.StatsdClient, conf.Log, conf.ShuttingDown)

		configToReturn = conf
		return nil
	}

	err := app.Run(args)

	return configToReturn, err
}
