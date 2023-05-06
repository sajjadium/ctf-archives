package smokescreen

import (
	"context"
	"crypto/tls"
	"crypto/x509"
	"crypto/x509/pkix"
	"encoding/asn1"
	"encoding/hex"
	"encoding/pem"
	"errors"
	"fmt"
	"io/ioutil"
	"net"
	"net/http"
	"os"
	"strconv"
	"sync/atomic"
	"time"

	log "github.com/sirupsen/logrus"
	acl "github.com/stripe/smokescreen/pkg/smokescreen/acl/v1"
	"github.com/stripe/smokescreen/pkg/smokescreen/conntrack"
)

type RuleRange struct {
	Net  net.IPNet
	Port int
}

type Config struct {
	Ip                           string
	Port                         uint16
	Listener                     net.Listener
	DenyRanges                   []RuleRange
	AllowRanges                  []RuleRange
	Resolver                     *net.Resolver
	ConnectTimeout               time.Duration
	ExitTimeout                  time.Duration
	MetricsClient                *MetricsClient
	EgressACL                    acl.Decider
	SupportProxyProtocol         bool
	TlsConfig                    *tls.Config
	CrlByAuthorityKeyId          map[string]*pkix.CertificateList
	RoleFromRequest              func(subject *http.Request) (string, error)
	clientCasBySubjectKeyId      map[string]*x509.Certificate
	AdditionalErrorMessageOnDeny string
	Log                          *log.Logger
	DisabledAclPolicyActions     []string
	AllowMissingRole             bool
	StatsSocketDir               string
	StatsSocketFileMode          os.FileMode
	StatsServer                  *StatsServer // StatsServer
	ConnTracker                  *conntrack.Tracker
	Healthcheck                  http.Handler // User defined http.Handler for optional requests to a /healthcheck endpoint
	ShuttingDown                 atomic.Value // Stores a boolean value indicating whether the proxy is actively shutting down

	// Network type to use when performing DNS lookups. Must be one of "ip", "ip4" or "ip6".
	Network string

	// A connection is idle if it has been inactive (no bytes in/out) for this many seconds.
	IdleTimeout time.Duration

	// These are *only* used for traditional HTTP proxy requests
	TransportMaxIdleConns        int
	TransportMaxIdleConnsPerHost int

	// Used for logging connection time
	TimeConnect bool

	// Custom Dial Timeout function to be called
	ProxyDialTimeout func(ctx context.Context, network, address string, timeout time.Duration) (net.Conn, error)

	// Customer handler to allow clients to modify reject responses
	RejectResponseHandler func(*http.Response)

	// UnsafeAllowPrivateRanges inverts the default behavior, telling smokescreen to allow private IP
	// ranges by default (exempting loopback and unicast ranges)
	// This setting can be used to configure Smokescreen with a blocklist, rather than an allowlist
	UnsafeAllowPrivateRanges bool
}

type missingRoleError struct {
	error
}

func MissingRoleError(s string) error {
	return missingRoleError{errors.New(s)}
}

func IsMissingRoleError(err error) bool {
	_, ok := err.(missingRoleError)
	return ok
}

func parseRanges(rangeStrings []string) ([]RuleRange, error) {
	outRanges := make([]RuleRange, len(rangeStrings))
	for i, str := range rangeStrings {
		_, ipnet, err := net.ParseCIDR(str)
		if err != nil {
			return outRanges, err
		}
		outRanges[i].Net = *ipnet
	}
	return outRanges, nil
}

func parseAddresses(addressStrings []string) ([]RuleRange, error) {
	outRanges := make([]RuleRange, len(addressStrings))
	for i, str := range addressStrings {
		ip := net.ParseIP(str)
		if ip == nil {
			ipStr, portStr, err := net.SplitHostPort(str)
			if err != nil {
				return outRanges, fmt.Errorf("address must be in the form ip[:port], got %s", str)
			}

			ip = net.ParseIP(ipStr)
			if ip == nil {
				return outRanges, fmt.Errorf("invalid IP address '%s'", ipStr)
			}

			port, err := strconv.Atoi(portStr)
			if err != nil {
				return outRanges, fmt.Errorf("invalid port number '%s'", portStr)
			}

			outRanges[i].Port = port
		}

		var mask net.IPMask
		if ip.To4() != nil {
			mask = net.CIDRMask(32, 32)
		} else {
			mask = net.CIDRMask(128, 128)
		}

		outRanges[i].Net = net.IPNet{
			IP:   ip,
			Mask: mask,
		}
	}
	return outRanges, nil
}

func (config *Config) SetDenyRanges(rangeStrings []string) error {
	var err error
	ranges, err := parseRanges(rangeStrings)
	if err != nil {
		return err
	}
	config.DenyRanges = append(config.DenyRanges, ranges...)
	return nil
}

func (config *Config) SetAllowRanges(rangeStrings []string) error {
	var err error
	ranges, err := parseRanges(rangeStrings)
	if err != nil {
		return err
	}
	config.AllowRanges = append(config.AllowRanges, ranges...)
	return nil
}

func (config *Config) SetDenyAddresses(addressStrings []string) error {
	var err error
	ranges, err := parseAddresses(addressStrings)
	if err != nil {
		return err
	}
	config.DenyRanges = append(config.DenyRanges, ranges...)
	return nil
}

func (config *Config) SetAllowAddresses(addressStrings []string) error {
	var err error
	ranges, err := parseAddresses(addressStrings)
	if err != nil {
		return err
	}
	config.AllowRanges = append(config.AllowRanges, ranges...)
	return nil
}

func (config *Config) SetResolverAddresses(resolverAddresses []string) error {
	// TODO: support round-robin between multiple addresses
	if len(resolverAddresses) > 1 {
		return fmt.Errorf("only one resolver address allowed, %d provided", len(resolverAddresses))
	}

	// No resolver specified, use the system resolver
	if len(resolverAddresses) == 0 {
		return nil
	}

	addr := resolverAddresses[0]
	_, _, err := net.SplitHostPort(addr)
	if err != nil {
		return err
	}

	r := net.Resolver{
		PreferGo: true,
		Dial: func(ctx context.Context, _, _ string) (net.Conn, error) {
			d := net.Dialer{}
			return d.DialContext(ctx, "udp", addr)
		},
	}
	config.Resolver = &r
	return nil
}

// RFC 5280,  4.2.1.1
type authKeyId struct {
	Id []byte `asn1:"optional,tag:0"`
}

func NewConfig() *Config {
	log.SetFormatter(&log.JSONFormatter{
		TimestampFormat: time.RFC3339Nano,
	})

	return &Config{
		CrlByAuthorityKeyId:     make(map[string]*pkix.CertificateList),
		clientCasBySubjectKeyId: make(map[string]*x509.Certificate),
		Log:                     log.New(),
		Port:                    4750,
		ExitTimeout:             500 * time.Minute,
		StatsSocketFileMode:     os.FileMode(0700),
		ShuttingDown:            atomic.Value{},
		MetricsClient:           NewNoOpMetricsClient(),
		Network:                 "ip",
	}
}

func (config *Config) SetupCrls(crlFiles []string) error {
	for _, crlFile := range crlFiles {
		crlBytes, err := ioutil.ReadFile(crlFile)
		if err != nil {
			return err
		}

		certList, err := x509.ParseCRL(crlBytes)
		if err != nil {
			log.Printf("Failed to parse CRL in '%s': %#v\n", crlFile, err)
		}

		// find the X509v3 Authority Key Identifier in the extensions (2.5.29.35)
		crlIssuerId := ""
		extensionOid := []int{2, 5, 29, 35}
		for _, v := range certList.TBSCertList.Extensions {
			if v.Id.Equal(extensionOid) { // Hurray, we found it
				// Boo, it's ASN.1.
				var crlAuthorityKey authKeyId
				_, err := asn1.Unmarshal(v.Value, &crlAuthorityKey)
				if err != nil {
					fmt.Printf("error: Failed to read AuthorityKey: %#v\n", err)
					continue
				}
				crlIssuerId = string(crlAuthorityKey.Id)
				break
			}
		}
		if crlIssuerId == "" {
			log.Print(fmt.Errorf("error: CRL from '%s' has no Authority Key Identifier: ignoring it\n", crlFile))
			continue
		}

		// Make sure we have a CA for this CRL or warn
		caCert, ok := config.clientCasBySubjectKeyId[crlIssuerId]

		if !ok {
			log.Printf("warn: CRL loaded for issuer '%s' but no such CA loaded: ignoring it\n", hex.EncodeToString([]byte(crlIssuerId)))
			fmt.Printf("%#v loaded certs\n", len(config.clientCasBySubjectKeyId))
			continue
		}

		// At this point, we have the CA certificate and the CRL. All that's left before evicting the CRL we currently trust is to verify the new CRL's signature
		err = caCert.CheckCRLSignature(certList)
		if err != nil {
			fmt.Printf("error: Could not trust CRL. Error during signature check: %#v\n", err)
			continue
		}

		// At this point, we have a new CRL which we trust. Let's evict the old one.
		config.CrlByAuthorityKeyId[crlIssuerId] = certList
		fmt.Printf("info: Loaded CRL for Authority ID '%s'\n", hex.EncodeToString([]byte(crlIssuerId)))
	}

	// Verify that all CAs loaded have a CRL
	for k := range config.clientCasBySubjectKeyId {
		_, ok := config.CrlByAuthorityKeyId[k]
		if !ok {
			fmt.Printf("warn: no CRL loaded for Authority ID '%s'\n", hex.EncodeToString([]byte(k)))
		}
	}
	return nil
}

func (config *Config) SetupStatsdWithNamespace(addr, namespace string) error {
	if addr == "" {
		fmt.Println("warn: no statsd addr provided, using noop client")
		config.MetricsClient = NewNoOpMetricsClient()
		return nil
	}

	mc, err := NewMetricsClient(addr, namespace)
	if err != nil {
		return err
	}
	config.MetricsClient = mc
	return nil
}

func (config *Config) SetupStatsd(addr string) error {
	return config.SetupStatsdWithNamespace(addr, DefaultStatsdNamespace)
}

func (config *Config) SetupEgressAcl(aclFile string) error {
	if aclFile == "" {
		config.EgressACL = nil
		return nil
	}

	log.Printf("Loading egress ACL from %s", aclFile)

	egressACL, err := acl.New(config.Log, acl.NewYAMLLoader(aclFile), config.DisabledAclPolicyActions)
	if err != nil {
		log.Print(err)
		return err
	}
	config.EgressACL = egressACL

	return nil
}

func addCertsFromFile(config *Config, pool *x509.CertPool, fileName string) error {
	data, err := ioutil.ReadFile(fileName)

	//TODO this is a bit awkward
	config.populateClientCaMap(data)

	if err != nil {
		return err
	}
	ok := pool.AppendCertsFromPEM(data)
	if !ok {
		return fmt.Errorf("Failed to load any certificates from file '%s'", fileName)
	}
	return nil
}

// certFile and keyFile may be the same file containing concatenated PEM blocks
func (config *Config) SetupTls(certFile, keyFile string, clientCAFiles []string) error {
	if certFile == "" || keyFile == "" {
		return errors.New("both certificate and key files must be specified to set up TLS")
	}

	serverCert, err := tls.LoadX509KeyPair(certFile, keyFile)
	if err != nil {
		return err
	}

	clientAuth := tls.NoClientCert
	clientCAs := x509.NewCertPool()

	if len(clientCAFiles) != 0 {
		clientAuth = tls.VerifyClientCertIfGiven
		for _, caFile := range clientCAFiles {
			err = addCertsFromFile(config, clientCAs, caFile)
			if err != nil {
				return err
			}
		}
	}

	config.TlsConfig = &tls.Config{
		Certificates: []tls.Certificate{serverCert},
		ClientAuth:   clientAuth,
		ClientCAs:    clientCAs,
	}

	return nil
}

func (config *Config) populateClientCaMap(pemCerts []byte) (ok bool) {

	for len(pemCerts) > 0 {
		var block *pem.Block
		block, pemCerts = pem.Decode(pemCerts)
		if block == nil {
			break
		}
		if block.Type != "CERTIFICATE" || len(block.Headers) != 0 {
			continue
		}

		cert, err := x509.ParseCertificate(block.Bytes)
		if err != nil {
			continue
		}
		fmt.Printf("info: Loaded CA with Authority ID '%s'\n", hex.EncodeToString(cert.SubjectKeyId))
		config.clientCasBySubjectKeyId[string(cert.SubjectKeyId)] = cert
		ok = true
	}
	return
}
