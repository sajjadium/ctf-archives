//go:build !nointegration
// +build !nointegration

package cmd

import (
	"bufio"
	"context"
	"crypto/tls"
	"crypto/x509"
	"errors"
	"fmt"
	"io"
	"io/ioutil"
	"math/rand"
	"net"
	"net/http"
	"net/http/httptest"
	"net/url"
	"os"
	"testing"
	"time"

	"github.com/hashicorp/go-cleanhttp"
	"github.com/sirupsen/logrus"
	logrustest "github.com/sirupsen/logrus/hooks/test"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/stripe/smokescreen/pkg/smokescreen"
	acl "github.com/stripe/smokescreen/pkg/smokescreen/acl/v1"
)

var ProxyTargetHandler = http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
	time.Sleep(50 * time.Millisecond)
	io.WriteString(w, "okok")
})

// RoleFromRequest implementations
func testRFRHeader(req *http.Request) (string, error) {
	idHeader := req.Header["X-Smokescreen-Role"]
	if len(idHeader) != 1 {
		return "", smokescreen.MissingRoleError(fmt.Sprintf("Expected 1 header, got %d", len(idHeader)))
	}
	return idHeader[0], nil
}
func testRFRCert(req *http.Request) (string, error) {
	if len(req.TLS.PeerCertificates) == 0 {
		return "", smokescreen.MissingRoleError("client did not provide certificate")
	}
	return req.TLS.PeerCertificates[0].Subject.CommonName, nil
}

type TestCase struct {
	ExpectAllow   bool
	Action        acl.EnforcementPolicy
	ExpectStatus  int
	OverTLS       bool
	OverConnect   bool
	ProxyURL      string
	RandomTrace   int
	TargetURL     string
	RoleName      string
	UpstreamProxy string
}

// validateProxyResponse validates tests cases and expected responses from TestSmokescreenIntegration
func validateProxyResponse(t *testing.T, test *TestCase, resp *http.Response, err error, logs []*logrus.Entry) {
	t.Logf("HTTP Response: %#v", resp)

	a := assert.New(t)
	if test.ExpectAllow {
		// In some cases we expect the proxy to allow the request but the upstream to return an error
		if test.ExpectStatus != 0 {
			if resp == nil {
				t.Fatal(err)
			}
			a.Equal(test.ExpectStatus, resp.StatusCode, "Expected HTTP response code did not match")
			return
		}
		// CONNECT requests which return a non-200 return an error and a nil response
		if resp == nil {
			a.Error(err)
			return
		}
		a.Equal(test.ExpectStatus, resp.StatusCode, "HTTP Response code should indicate success.")
	} else {
		// CONNECT requests which return a non-200 return an error and a nil response
		if resp == nil {
			a.Error(err)
			return
		}
		// If there is a response returned, it should contain smokescreen's error message
		body, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			t.Fatal(err)
		}
		defer resp.Body.Close()
		a.Contains(string(body), "denied")
		a.Contains(string(body), "additional_error_message_validation_key")
		a.Equal(test.ExpectStatus, resp.StatusCode, "Expected status did not match actual response code")
	}

	var entries []*logrus.Entry
	entries = append(entries, logs...)

	if len(entries) > 0 {
		entry := findLogEntry(entries, smokescreen.CanonicalProxyDecision)
		a.NotNil(entry)
		a.Equal(entry.Message, smokescreen.CanonicalProxyDecision)

		a.Contains(entry.Data, "allow")
		a.Equal(test.ExpectAllow, entry.Data["allow"])

		a.Contains(entry.Data, "proxy_type")
		if test.OverConnect {
			a.Equal("connect", entry.Data["proxy_type"])
		} else {
			a.Equal("http", entry.Data["proxy_type"])
		}

		a.Contains(entry.Data, "requested_host")
		u, _ := url.Parse(test.TargetURL)
		a.Equal(fmt.Sprintf("%s:%s", u.Hostname(), u.Port()), entry.Data["requested_host"])
	}
}

func generateRoleForPolicy(action acl.EnforcementPolicy) string {
	switch action {
	case acl.Open:
		return "open"
	case acl.Report:
		return "report"
	case acl.Enforce:
		return "enforce"
	}
	panic("unknown-mode")
}

func generateClientForTest(t *testing.T, test *TestCase) *http.Client {
	a := assert.New(t)

	var client *http.Client
	proxyURL, err := url.Parse(test.ProxyURL)
	if err != nil {
		t.Fatal(err)
	}

	if test.OverConnect {
		client = cleanhttp.DefaultClient()
		client.Transport.(*http.Transport).DialContext =
			func(ctx context.Context, network, addr string) (net.Conn, error) {
				var conn net.Conn

				connectProxyReq, err := http.NewRequest(
					"CONNECT",
					test.TargetURL,
					nil)
				if err != nil {
					return nil, err
				}

				if test.OverTLS {
					var certs []tls.Certificate

					// Load client cert for role
					if test.RoleName != "" {
						certPath := fmt.Sprintf("testdata/pki/%s-client.pem", test.RoleName)
						keyPath := fmt.Sprintf("testdata/pki/%s-client-key.pem", test.RoleName)
						cert, err := tls.LoadX509KeyPair(certPath, keyPath)
						if err != nil {
							return nil, err
						}
						certs = append(certs, cert)
					}

					caBytes, err := ioutil.ReadFile("testdata/pki/ca.pem")
					if err != nil {
						return nil, err
					}
					caPool := x509.NewCertPool()
					a.True(caPool.AppendCertsFromPEM(caBytes))

					proxyTLSClientConfig := tls.Config{
						Certificates: certs,
						RootCAs:      caPool,
					}
					connRaw, err := tls.Dial("tcp", proxyURL.Host, &proxyTLSClientConfig)
					if err != nil {
						return nil, err
					}
					conn = connRaw
				} else {
					connRaw, err := net.Dial(network, proxyURL.Host)
					if err != nil {
						return nil, err
					}
					conn = connRaw

					// If we're not talking to the proxy over TLS, let's use headers as identifiers
					connectProxyReq.Header.Add("X-Smokescreen-Role", "egressneedingservice-"+test.RoleName)
					connectProxyReq.Header.Add("X-Smokescreen-Trace-ID", fmt.Sprintf("%d", test.RandomTrace))
				}

				t.Logf("connect request: %#v", connectProxyReq)
				connectProxyReq.Write(conn)

				// Read the response from the connect request and return an error for any non-200
				// from smokescreen
				br := bufio.NewReader(conn)
				resp, err := http.ReadResponse(br, connectProxyReq)
				if err != nil {
					conn.Close()
					return nil, err
				}
				defer resp.Body.Close()
				if resp.StatusCode != http.StatusOK {
					resp, err := ioutil.ReadAll(resp.Body)
					if err != nil {
						return nil, err
					}
					conn.Close()
					return nil, errors.New(string(resp))
				}
				return conn, nil
			}
	} else {
		client = &http.Client{
			Transport: &http.Transport{
				Proxy: http.ProxyURL(proxyURL),
			},
		}
	}

	client.Transport.(*http.Transport).TLSClientConfig = &tls.Config{InsecureSkipVerify: true}

	return client
}

func generateRequestForTest(t *testing.T, test *TestCase) *http.Request {
	a := assert.New(t)

	req, err := http.NewRequest("GET", test.TargetURL, nil)
	a.NoError(err)

	if !test.OverTLS && !test.OverConnect {
		// If we're not talking to the proxy over TLS, let's use headers as identifiers
		req.Header.Add("X-Smokescreen-Role", "egressneedingservice-"+test.RoleName)
		req.Header.Add("X-Smokescreen-Trace-ID", fmt.Sprintf("%d", test.RandomTrace))
	}

	t.Logf("HTTP Request: %#v", req)
	return req
}

func executeRequestForTest(t *testing.T, test *TestCase, logHook *logrustest.Hook) (*http.Response, error) {
	t.Logf("Executing Request for test case %#v", test)

	logHook.Reset()

	client := generateClientForTest(t, test)
	req := generateRequestForTest(t, test)

	return client.Do(req)
}

func TestSmokescreenIntegration(t *testing.T) {
	var logHook logrustest.Hook

	// Holds TLS and non-TLS enabled local HTTP servers
	httpServers := map[bool]*httptest.Server{}

	// Holds TLS and non-TLS enabled Smokescreen instances
	proxyServers := map[bool]*httptest.Server{}

	// Contains http and https URLs to api.github.com
	externalHosts := make(map[bool]string)

	for _, useTLS := range []bool{true, false} {
		// Smokescreen instances
		_, proxyServer, err := startSmokescreen(t, useTLS, &logHook)
		require.NoError(t, err)
		defer proxyServer.Close()
		proxyServers[useTLS] = proxyServer

		if useTLS {
			externalHosts[useTLS] = "https://api.stripe.com:443"

			httpServer := httptest.NewTLSServer(ProxyTargetHandler)
			defer httpServer.Close()
			httpServers[useTLS] = httpServer
		} else {
			// Must specify a domain which won't redirect to HTTPS
			externalHosts[useTLS] = "http://checkip.amazonaws.com:80"

			httpServer := httptest.NewServer(ProxyTargetHandler)
			defer httpServer.Close()
			httpServers[useTLS] = httpServer
		}
	}

	// Send the proxy request via TLS
	overTLSOptions := []bool{true, false}

	// Send the proxy request using CONNECT
	overConnectOptions := []bool{true, false}

	// If the proxy target should be sent to an authorized host
	authorizedHosts := []bool{true, false}

	enforcementPolicies := []acl.EnforcementPolicy{
		acl.Enforce,
		acl.Report,
		acl.Open,
	}

	var testCases []*TestCase

	// This generates all the permutations for the common test cases
	// * proxy requests using CONNECT and regular HTTP proxy
	// * TLS and non-TLS proxy targets
	// * hosts authorized and not authorized by the config in testdata/sample_config.yaml
	// * enforce, report, and open enforcement policies
	for _, overConnect := range overConnectOptions {
		for _, overTLS := range overTLSOptions {
			// Explicitly do not support these test cases
			// 1) You cannot tunnel TLS using a traditional HTTP proxy request
			// 2) If you attempt to tunnel a non-TLS HTTP request using CONNECT,
			//    Go's HTTP machinery rewrites the scheme as HTTPS.
			if (overTLS && !overConnect) || (!overTLS && overConnect) {
				continue
			}

			// An authorizedHost indicates the request should be sent to our
			// local HTTP server. If authorizedHost is false, the request
			// will be sent to api.github.com and may or may not be allowed
			// depending on the acl.EnforcementPolicy.
			for _, authorizedHost := range authorizedHosts {
				var proxyTarget string
				if authorizedHost {
					proxyTarget = httpServers[overTLS].URL
				} else {
					proxyTarget = externalHosts[overTLS]
				}

				for _, policy := range enforcementPolicies {
					var expectAllow bool
					// If a host is authorized, it is allowed by the config
					// and will always be allowed.
					if authorizedHost {
						expectAllow = true
					}

					// Report and open modes should always allow requests.
					if policy != acl.Enforce {
						expectAllow = true
					}

					testCase := &TestCase{
						ExpectAllow: expectAllow,
						Action:      policy,
						OverTLS:     overTLS,
						OverConnect: overConnect,
						ProxyURL:    proxyServers[overTLS].URL,
						TargetURL:   proxyTarget,
						RoleName:    generateRoleForPolicy(policy),
					}

					if expectAllow {
						testCase.ExpectStatus = http.StatusOK
						if overTLS && !authorizedHost {
							// The Stripe API returns a 404 to a bare HTTP GET request
							testCase.ExpectStatus = http.StatusNotFound
						}
					} else {
						testCase.ExpectStatus = http.StatusProxyAuthRequired
					}
					testCases = append(testCases, testCase)
				}
			}
		}

		baseCase := TestCase{
			OverTLS:     false,
			OverConnect: overConnect,
			ProxyURL:    proxyServers[false].URL,
		}

		// Empty roles should default deny per the test config
		noRoleDenyCase := baseCase
		noRoleDenyCase.TargetURL = httpServers[baseCase.OverTLS].URL
		noRoleDenyCase.ExpectAllow = false
		noRoleDenyCase.ExpectStatus = http.StatusProxyAuthRequired

		// Unknown roles should default deny per the test config
		unknownRoleDenyCase := baseCase
		unknownRoleDenyCase.TargetURL = httpServers[baseCase.OverTLS].URL
		unknownRoleDenyCase.RoleName = "unknown"
		unknownRoleDenyCase.ExpectAllow = false
		unknownRoleDenyCase.ExpectStatus = http.StatusProxyAuthRequired

		// This must be a global unicast, non-loopback address or other IP rules will
		// block it regardless of the specific configuration we're trying to test.
		badIPRangeCase := baseCase
		badIPRangeCase.TargetURL = "http://1.1.1.1:80"
		badIPRangeCase.ExpectAllow = false
		badIPRangeCase.ExpectStatus = http.StatusProxyAuthRequired
		badIPRangeCase.RoleName = generateRoleForPolicy(acl.Open)

		// This must be a global unicast, non-loopback address or other IP rules will
		// block it regardless of the specific configuration we're trying to test.
		badIPAddressCase := baseCase
		badIPAddressCase.TargetURL = "http://1.0.0.1:123"
		badIPAddressCase.ExpectAllow = false
		badIPAddressCase.ExpectStatus = http.StatusProxyAuthRequired
		badIPAddressCase.RoleName = generateRoleForPolicy(acl.Open)

		testCases = append(testCases,
			&unknownRoleDenyCase, &noRoleDenyCase,
			&badIPRangeCase, &badIPAddressCase,
		)
	}

	for _, testCase := range testCases {
		t.Run("", func(t *testing.T) {
			testCase.RandomTrace = rand.Int()
			resp, err := executeRequestForTest(t, testCase, &logHook)
			validateProxyResponse(t, testCase, resp, err, logHook.AllEntries())
		})
	}
}

// validateProxyResponseWithUpstream validates tests cases and expected responses
// from TestUpstreamProxySmokescreenIntegration. This validates that requests
// sent to a smokescreen instance with an additional upstream proxy set
// (proxy chaining) forwards the request to the next proxy hop instead of directly
// to the proxy target.
func validateProxyResponseWithUpstream(t *testing.T, test *TestCase, resp *http.Response, err error, logs []*logrus.Entry) {
	a := assert.New(t)
	t.Logf("HTTP Response: %#v", resp)

	if test.OverConnect {
		a.Contains(err.Error(), "Failed to connect to remote host")
	} else {
		a.Equal(http.StatusBadGateway, resp.StatusCode)
	}
}

// This test must be run with a separate test command as the environment variables
// required can race with the test above.
func TestInvalidUpstreamProxyConfiguration(t *testing.T) {
	var logHook logrustest.Hook
	servers := map[bool]*httptest.Server{}

	// Create TLS and non-TLS instances of Smokescreen
	for _, useTLS := range []bool{true, false} {
		_, server, err := startSmokescreen(t, useTLS, &logHook)
		require.NoError(t, err)
		defer server.Close()
		servers[useTLS] = server
	}

	// Passing an illegal upstream proxy value is not designed to be an especially well
	// handled error so it would fail many of the checks in our other tests. We really
	// only care to ensure that these requests never succeed.
	for _, overConnect := range []bool{true, false} {
		t.Run(fmt.Sprintf("illegal proxy with CONNECT %t", overConnect), func(t *testing.T) {
			var proxyTarget string
			var upstreamProxy string

			// These proxy targets don't actually matter as the requests won't be sent.
			// because the resolution of the upstream proxy will fail.
			if overConnect {
				upstreamProxy = "https://notaproxy.prxy.svc:443"
				proxyTarget = "https://api.stripe.com:443"
			} else {
				upstreamProxy = "http://notaproxy.prxy.svc:80"
				proxyTarget = "http://checkip.amazonaws.com:80"
			}

			testCase := &TestCase{
				OverConnect:   overConnect,
				OverTLS:       overConnect,
				ProxyURL:      servers[overConnect].URL,
				TargetURL:     proxyTarget,
				UpstreamProxy: upstreamProxy,
				RoleName:      generateRoleForPolicy(acl.Open),
				ExpectStatus:  http.StatusBadGateway,
			}
			os.Setenv("http_proxy", testCase.UpstreamProxy)
			os.Setenv("https_proxy", testCase.UpstreamProxy)

			resp, err := executeRequestForTest(t, testCase, &logHook)
			validateProxyResponseWithUpstream(t, testCase, resp, err, logHook.AllEntries())

			os.Unsetenv("http_proxy")
			os.Unsetenv("https_proxy")
		})
	}
}

func TestClientHalfCloseConnection(t *testing.T) {
	a := assert.New(t)

	h := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "TCP is great!")
	})
	remote := httptest.NewServer(h)

	var logHook logrustest.Hook

	conf, server, err := startSmokescreen(t, false, &logHook)
	require.NoError(t, err)
	defer server.Close()

	proxyCon, err := net.Dial("tcp", server.Listener.Addr().String())
	if err != nil {
		t.Error(err)
	}

	// Send the CONNECT request to Smokescreen
	conReq, err := http.NewRequest("CONNECT", remote.URL, nil)
	if err != nil {
		t.Error(err)
	}
	conReq.Header.Add("X-Smokescreen-Role", "egressneedingservice-open")
	if err := conReq.Write(proxyCon); err != nil {
		t.Error(err)
	}

	buf := bufio.NewReader(proxyCon)
	resp, err := http.ReadResponse(buf, conReq)
	if err != nil {
		t.Error(err)
	}

	a.Equal(resp.StatusCode, http.StatusOK)

	// Send the response to the "remote" server
	req, err := http.NewRequest("GET", remote.URL, nil)
	if err != nil {
		t.Error(err)
	}
	if err := req.Write(proxyCon); err != nil {
		t.Error(err)
	}
	resp, err = http.ReadResponse(buf, req)
	if err != nil {
		t.Error(err)
	}
	a.Equal(resp.StatusCode, http.StatusOK)

	// Unwrap the underlying net.TCPConn
	tcpConn, ok := proxyCon.(*net.TCPConn)
	if !ok {
		t.Error("conn did not unwrap to net.TCPConn")
	}

	// Now half close the connection and check that Smokescreen
	// logged a connection close event
	tcpConn.CloseWrite()

	conf.ConnTracker.Wg.Wait()

	entries := logHook.AllEntries()
	entry := findLogEntry(entries, "CANONICAL-PROXY-CN-CLOSE")
	a.NotNil(entry)
}

func findLogEntry(entries []*logrus.Entry, msg string) *logrus.Entry {
	for _, entry := range entries {
		if entry.Message == msg {
			return entry
		}
	}
	return nil
}

func startSmokescreen(t *testing.T, useTLS bool, logHook logrus.Hook) (*smokescreen.Config, *httptest.Server, error) {
	args := []string{
		"smokescreen",
		"--listen-ip=127.0.0.1",
		"--egress-acl-file=testdata/sample_config.yaml",
		"--additional-error-message-on-deny=additional_error_message_validation_key",
		"--deny-range=1.1.1.1/32",
		"--allow-range=127.0.0.1/32",
		"--deny-address=1.0.0.1:123",
	}

	if useTLS {
		args = append(args,
			"--tls-server-bundle-file=testdata/pki/server-bundle.pem",
			"--tls-client-ca-file=testdata/pki/ca.pem",
			"--tls-crl-file=testdata/pki/crl.pem",
		)
	}

	conf, err := NewConfiguration(args, nil)
	if err != nil {
		t.Fatalf("Failed to create configuration: %v", err)
	}

	if useTLS {
		conf.RoleFromRequest = testRFRCert
	} else {
		conf.RoleFromRequest = testRFRHeader
	}

	conf.MetricsClient = smokescreen.NewNoOpMetricsClient()

	conf.ConnectTimeout = time.Second

	fmt.Printf("2 %#v\n", conf)
	conf.Log.AddHook(logHook)

	handler := smokescreen.BuildProxy(conf)
	server := httptest.NewUnstartedServer(handler)

	if useTLS {
		server.TLS = conf.TlsConfig
		server.StartTLS()
	} else {
		server.Start()
	}

	return conf, server, nil
}
