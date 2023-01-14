package main

import (
	"bufio"
	"bytes"
	"context"
	"crypto/sha256"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"io/ioutil"
	"math/rand"
	"net/http"
	"os"
	"time"
)

var password = sha256.Sum256([]byte("idek"))
var randomData []byte

const (
	MaxOrders = 10
)

func initRandomData() {
	rand.Seed(1337)
	randomData = make([]byte, 24576)
	if _, err := rand.Read(randomData); err != nil {
		panic(err)
	}
	copy(randomData[12625:], password[:])
}

type ReadOrderReq struct {
	Orders []int `json:"orders"`
}

func justReadIt(w http.ResponseWriter, r *http.Request) {
	defer r.Body.Close()

	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		w.WriteHeader(500)
		w.Write([]byte("bad request\n"))
		return
	}

	reqData := ReadOrderReq{}
	if err := json.Unmarshal(body, &reqData); err != nil {
		w.WriteHeader(500)
		w.Write([]byte("invalid body\n"))
		return
	}

	if len(reqData.Orders) > MaxOrders {
		w.WriteHeader(500)
		w.Write([]byte("whoa there, max 10 orders!\n"))
		return
	}

	reader := bytes.NewReader(randomData)
	validator := NewValidator()

	ctx := context.Background()
	for _, o := range reqData.Orders {
		if err := validator.CheckReadOrder(o); err != nil {
			w.WriteHeader(500)
			w.Write([]byte(fmt.Sprintf("error: %v\n", err)))
			return
		}

		ctx = WithValidatorCtx(ctx, reader, int(o))
		_, err := validator.Read(ctx)
		if err != nil {
			w.WriteHeader(500)
			w.Write([]byte(fmt.Sprintf("failed to read: %v\n", err)))
			return
		}
	}

	if err := validator.Validate(ctx); err != nil {
		w.WriteHeader(500)
		w.Write([]byte(fmt.Sprintf("validation failed: %v\n", err)))
		return
	}

	w.WriteHeader(200)
	w.Write([]byte(os.Getenv("FLAG")))
}

func main() {
	if _, exists := os.LookupEnv("LISTEN_ADDR"); !exists {
		panic("env LISTEN_ADDR is required")
	}
	if _, exists := os.LookupEnv("FLAG"); !exists {
		panic("env FLAG is required")
	}

	initRandomData()

	http.HandleFunc("/just-read-it", justReadIt)

	srv := http.Server{
		Addr:         os.Getenv("LISTEN_ADDR"),
		ReadTimeout:  5 * time.Second,
		WriteTimeout: 5 * time.Second,
	}

	fmt.Printf("Server listening on %s\n", os.Getenv("LISTEN_ADDR"))
	if err := srv.ListenAndServe(); err != nil {
		panic(err)
	}
}

type Validator struct{}

func NewValidator() *Validator {
	return &Validator{}
}

func (v *Validator) CheckReadOrder(o int) error {
	if o <= 0 || o > 100 {
		return fmt.Errorf("invalid order %v", o)
	}
	return nil
}

func (v *Validator) Read(ctx context.Context) ([]byte, error) {
	r, s := GetValidatorCtxData(ctx)
	buf := make([]byte, s)
	_, err := r.Read(buf)
	if err != nil {
		return nil, fmt.Errorf("read error: %v", err)
	}
	return buf, nil
}

func (v *Validator) Validate(ctx context.Context) error {
	r, _ := GetValidatorCtxData(ctx)
	buf, err := v.Read(WithValidatorCtx(ctx, r, 32))
	if err != nil {
		return err
	}
	if bytes.Compare(buf, password[:]) != 0 {
		return errors.New("invalid password")
	}
	return nil
}

const (
	reqValReaderKey = "readerKey"
	reqValSizeKey   = "reqValSize"
)

func GetValidatorCtxData(ctx context.Context) (io.Reader, int) {
	reader := ctx.Value(reqValReaderKey).(io.Reader)
	size := ctx.Value(reqValSizeKey).(int)
	if size >= 100 {
		reader = bufio.NewReader(reader)
	}
	return reader, size
}

func WithValidatorCtx(ctx context.Context, r io.Reader, size int) context.Context {
	ctx = context.WithValue(ctx, reqValReaderKey, r)
	ctx = context.WithValue(ctx, reqValSizeKey, size)
	return ctx
}
