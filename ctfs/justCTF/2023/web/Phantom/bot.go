package main

import (
	"context"
	"crypto/rand"
	"encoding/base64"
	"flag"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/chromedp/chromedp"
)

func generateSecretString(length int) string {
	token := make([]byte, length)
	_, err := rand.Read(token)
	if err != nil {
		fmt.Println(err)
		return ""
	}
	return base64.StdEncoding.EncodeToString(token)
}

func main() {
	url := flag.String("url", "", "url")
	login := generateSecretString(16)
	pwd := generateSecretString(16)
	name := os.Getenv("FLAG")
	if name == "" {
		name = "testflag"
	}
	flag.Parse()
	log.Println("url:", *url)
	opts := append(chromedp.DefaultExecAllocatorOptions[:], chromedp.Flag("headless", true))
	alloCtx, cancel := chromedp.NewExecAllocator(context.Background(), opts...)
	defer cancel()

	ctx, cancel := chromedp.NewContext(alloCtx)
	ctx, cancel = context.WithTimeout(ctx, 5*time.Second)
	defer cancel()

	err := chromedp.Run(ctx, chromedp.Tasks{
		chromedp.Navigate("https://phantom.web.jctf.pro:443/signup"),
		chromedp.WaitVisible(`form`),
		chromedp.SendKeys(`input[name="username"]`, login),
		chromedp.SendKeys(`input[name="password"]`, pwd),
		chromedp.SendKeys(`input[name="name"]`, name),
		chromedp.Submit(`form`),
		chromedp.Navigate("https://phantom.web.jctf.pro:443/login"),
		chromedp.WaitVisible(`form`),
		chromedp.SendKeys(`input[name="username"]`, login),
		chromedp.SendKeys(`input[name="password"]`, pwd),
		chromedp.Submit(`form`),
		chromedp.Sleep(1 * time.Second),
		chromedp.Navigate(*url),
		chromedp.Sleep(5 * time.Second),
	})

	if err != nil {
		log.Fatal(err)
	}
}
