package main

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	"crypto/x509/pkix"
	"encoding/pem"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"math/big"
	"net/http"
	"os"
	"strconv"
	"sync/atomic"
	"time"

	"github.com/OpenPrinting/goipp"
)

const (
	address   = ":8631"
	printPath = "/ipp/print"
	certFile  = "cert.pem"
	keyFile   = "key.pem"
)

func init() {
	if err := initTLS(); err != nil {
		panic(err)
	}
}

func ippJobURI(jobID uint64) string {
	return fmt.Sprintf("ipps://localhost%v%v/job-%v", address, printPath, jobID)
}

func ippFindOperationAttribute(m *goipp.Message, name string) (goipp.Attribute, bool) {
	for _, opAttr := range m.Operation {
		if opAttr.Name == name {
			return opAttr, true
		}
	}
	return goipp.Attribute{}, false
}

func ippDefaultResponse(request *goipp.Message) *goipp.Message {
	response := goipp.NewResponse(goipp.DefaultVersion, goipp.StatusOk, request.RequestID)
	response.Operation.Add(goipp.MakeAttribute("attributes-charset", goipp.TagCharset, goipp.String("utf-8")))
	response.Operation.Add(goipp.MakeAttribute("attributes-natural-language", goipp.TagLanguage, goipp.String("en-US")))

	return response
}

var ippAttributes map[string]goipp.Attribute = ippPrinterAttributes()

func ippPrinterAttributes() map[string]goipp.Attribute {
	printerAttributes := map[string]goipp.Attribute{
		"printer-state":             goipp.MakeAttribute("printer-state", goipp.TagEnum, goipp.Integer(3 /* idle */)),
		"printer-state-reasons":     goipp.MakeAttribute("printer-state-reasons", goipp.TagKeyword, goipp.String("none")),
		"printer-is-accepting-jobs": goipp.MakeAttribute("printer-is-accepting-jobs", goipp.TagBoolean, goipp.Boolean(true)),
	}

	osAttr := goipp.Attribute{Name: "operations-supported"}
	osAttr.Values.Add(goipp.TagEnum, goipp.Integer(2 /* Print-Job */))
	osAttr.Values.Add(goipp.TagEnum, goipp.Integer(4 /* Validate-Job */))
	osAttr.Values.Add(goipp.TagEnum, goipp.Integer(5 /* Create-Job */))
	osAttr.Values.Add(goipp.TagEnum, goipp.Integer(6 /* Send-Document */))
	osAttr.Values.Add(goipp.TagEnum, goipp.Integer(8 /* Cancel-Job */))
	osAttr.Values.Add(goipp.TagEnum, goipp.Integer(9 /* Get-Job-Attributes */))
	osAttr.Values.Add(goipp.TagEnum, goipp.Integer(11 /* Get-Printer-Attributes */))
	printerAttributes[osAttr.Name] = osAttr

	dfsAttr := goipp.Attribute{Name: "document-format-supported"}
	dfsAttr.Values.Add(goipp.TagMimeType, goipp.String("application/pdf"))
	dfsAttr.Values.Add(goipp.TagMimeType, goipp.String("application/postscript"))
	dfsAttr.Values.Add(goipp.TagMimeType, goipp.String("image/jpeg"))
	dfsAttr.Values.Add(goipp.TagMimeType, goipp.String("text/plain"))
	printerAttributes[dfsAttr.Name] = dfsAttr

	pmjaAttr := goipp.Attribute{Name: "printer-mandatory-job-attributes"}
	printerAttributes[pmjaAttr.Name] = pmjaAttr

	return printerAttributes
}

func ippGetPrinterAttributes(request, response *goipp.Message) {
	opAttr, ok := ippFindOperationAttribute(request, "requested-attributes")
	if !ok {
		log.Printf("requested-attributes not found in request: %v\n", request)
		response.Code = goipp.Code(goipp.StatusErrorBadRequest)
		return
	}

	for _, reqAttr := range opAttr.Values {
		if printerAttr, ok := ippAttributes[reqAttr.V.String()]; ok {
			response.Printer.Add(printerAttr)
		} else {
			response.Unsupported.Add(goipp.MakeAttribute(reqAttr.V.String(), reqAttr.T, reqAttr.V))
			response.Code = goipp.Code(goipp.StatusOkIgnoredOrSubstituted)
		}
	}
}

func ippGetJobAttributes(request, response *goipp.Message) {
	jobIDAttr, ok := ippFindOperationAttribute(request, "job-id")
	if !ok {
		log.Printf("job-id not found in request: %v\n", request)
		response.Code = goipp.Code(goipp.StatusErrorBadRequest)
		return
	}

	var requestJobID uint64
	var err error
	if requestJobID, err = strconv.ParseUint(jobIDAttr.Values.String(), 10, 64); err != nil {
		log.Printf("Error parsing job-id value: %v\n", jobIDAttr.Values.String())
		response.Code = goipp.Code(goipp.StatusErrorBadRequest)
		return
	}

	opAttr, ok := ippFindOperationAttribute(request, "requested-attributes")
	if !ok {
		log.Printf("requested-attributes not found in request: %v\n", request)
		response.Code = goipp.Code(goipp.StatusErrorBadRequest)
		return
	}

	for _, reqAttr := range opAttr.Values {
		switch reqAttr.V.String() {
		case "job-id":
			response.Job.Add(goipp.MakeAttribute("job-id", goipp.TagInteger, goipp.Integer(requestJobID)))
		case "job-uri":
			response.Job.Add(goipp.MakeAttribute("job-uri", goipp.TagURI, goipp.String(ippJobURI(requestJobID))))
		case "job-state":
			response.Job.Add(goipp.MakeAttribute("job-state", goipp.TagEnum, goipp.Integer(9 /* completed */)))
		case "job-state-reasons":
			response.Job.Add(goipp.MakeAttribute("job-state-reasons", goipp.TagKeyword, goipp.String("job-completed-successfully")))
		default:
			response.Unsupported.Add(goipp.MakeAttribute(reqAttr.V.String(), reqAttr.T, reqAttr.V))
			response.Code = goipp.Code(goipp.StatusOkIgnoredOrSubstituted)
		}
	}
}

var jobIDCounter uint64

func ippCreateJob(request, response *goipp.Message) {
	jobID := atomic.AddUint64(&jobIDCounter, 1)

	response.Job.Add(goipp.MakeAttribute("job-id", goipp.TagInteger, goipp.Integer(jobID)))
	response.Job.Add(goipp.MakeAttribute("job-uri", goipp.TagURI, goipp.String(ippJobURI(jobID))))
	response.Job.Add(goipp.MakeAttribute("job-state", goipp.TagEnum, goipp.Integer(3 /* pending */)))
	response.Job.Add(goipp.MakeAttribute("job-state-reasons", goipp.TagKeyword, goipp.String("none")))
}

func ippSendDocument(request, response *goipp.Message, httpRequestBody io.ReadCloser) {
	data, err := ioutil.ReadAll(httpRequestBody)
	if err != nil {
		log.Printf("Error reading file from request body: %v\n", err)
		response.Code = goipp.Code(goipp.StatusErrorBadRequest)
		return
	}

	f, err := os.CreateTemp(".", "file")
	if err != nil {
		log.Printf("Error reading file from request body: %v\n", err)
		response.Code = goipp.Code(goipp.StatusErrorInternal)
		return
	}

	_, err = f.Write(data)
	if err != nil {
		log.Printf("Error writing file: %v\n", err)
		response.Code = goipp.Code(goipp.StatusErrorInternal)
		return
	}

	fmt.Println("Wrote file", f.Name())
}

func ippMakeResponse(request *goipp.Message, httpRequestBody io.ReadCloser) ([]byte, error) {
	response := ippDefaultResponse(request)

	switch goipp.Op(request.Code) {
	case goipp.OpGetPrinterAttributes:
		ippGetPrinterAttributes(request, response)
	case goipp.OpGetJobAttributes:
		ippGetJobAttributes(request, response)
	case goipp.OpCreateJob:
		ippCreateJob(request, response)
	case goipp.OpSendDocument:
		ippSendDocument(request, response, httpRequestBody)
	case goipp.OpPrintJob:
		ippCreateJob(request, response)
		ippSendDocument(request, response, httpRequestBody)
	default:
		// just send the default response
	}

	return response.EncodeBytes()
}

func print(w http.ResponseWriter, req *http.Request) {
	if req.URL.Path != "/ipp/print" {
		http.Error(w, "Not found", http.StatusNotFound)
		return
	}

	if req.Method != "POST" {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	m := &goipp.Message{}
	if err := m.Decode(req.Body); err != nil {
		http.Error(w, "Bad request", http.StatusBadRequest)
		return
	}

	if bytes, err := ippMakeResponse(m, req.Body); err == nil {
		w.Write(bytes)
		w.Header().Set("Content-Type", goipp.ContentType)
	} else {
		http.Error(w, "Internal server error", http.StatusInternalServerError)
		return
	}
}

func initTLS() error {
	certFileExists := false
	if _, err := os.Stat(certFile); err == nil {
		certFileExists = true
	}

	keyFileExists := false
	if _, err := os.Stat(keyFile); err == nil {
		keyFileExists = true
	}

	if certFileExists && keyFileExists {
		return nil
	}

	const bits = 2048

	var bigOne = big.NewInt(1)
	var bigTwo = big.NewInt(2)

	p, err := rand.Prime(rand.Reader, bits/2)
	if err != nil {
		return fmt.Errorf("failed to get prime: %w", err)
	}

	q := new(big.Int)
	q.Xor(p, new(big.Int).Lsh(bigOne, bits/2-3)) // ensure q is not close to p
	for {
		if q.ProbablyPrime(20) {
			break
		}
		switch q.Cmp(p) {
		case -1:
			q.Sub(q, bigTwo)
		case 1:
			q.Add(q, bigTwo)
		case 0: // should never happen
			return fmt.Errorf("failed to get prime: p == q")
		}
	}

	privateKey := &rsa.PrivateKey{}
	privateKey.Primes = []*big.Int{p, q}
	privateKey.N = new(big.Int).Mul(p, q)
	privateKey.E = 65537

	pminus1 := new(big.Int).Sub(p, bigOne)
	qminus1 := new(big.Int).Sub(q, bigOne)
	totient := new(big.Int).Mul(pminus1, qminus1)

	privateKey.D = new(big.Int)
	bigE := big.NewInt(int64(privateKey.E))
	ok := privateKey.D.ModInverse(bigE, totient)
	if ok == nil {
		return fmt.Errorf("failed prime number generation")
	}
	privateKey.Precompute()

	serialNumberLimit := new(big.Int).Lsh(big.NewInt(1), 128)
	serialNumber, err := rand.Int(rand.Reader, serialNumberLimit)
	if err != nil {
		return fmt.Errorf("failed to generate serial number: %w", err)
	}

	template := x509.Certificate{
		SerialNumber: serialNumber,
		Subject: pkix.Name{
			Organization: []string{"My Cool Printer"},
		},
		DNSNames:              []string{"localhost"},
		NotBefore:             time.Now(),
		NotAfter:              time.Now().Add(90 * 24 * time.Hour),
		KeyUsage:              x509.KeyUsageDigitalSignature,
		ExtKeyUsage:           []x509.ExtKeyUsage{x509.ExtKeyUsageServerAuth},
		BasicConstraintsValid: true,
	}

	certDERBytes, err := x509.CreateCertificate(rand.Reader, &template, &template, &privateKey.PublicKey, privateKey)
	if err != nil {
		return fmt.Errorf("failed to create certificate: %w", err)
	}

	certPEMBytes := pem.EncodeToMemory(&pem.Block{Type: "CERTIFICATE", Bytes: certDERBytes})
	if err := os.WriteFile(certFile, certPEMBytes, 0644); err != nil {
		return fmt.Errorf("failed to write certificate: %w", err)
	}

	keyDERBytes, err := x509.MarshalPKCS8PrivateKey(privateKey)
	if err != nil {
		return fmt.Errorf("failed to encode private key: %w", err)
	}

	keyPEMBytes := pem.EncodeToMemory(&pem.Block{Type: "PRIVATE KEY", Bytes: keyDERBytes})
	if err := os.WriteFile(keyFile, keyPEMBytes, 0600); err != nil {
		return fmt.Errorf("failed to write private key: %w", err)
	}

	return nil
}

func main() {
	http.HandleFunc(printPath, print)

	http.ListenAndServeTLS(address, certFile, keyFile, nil)
}
