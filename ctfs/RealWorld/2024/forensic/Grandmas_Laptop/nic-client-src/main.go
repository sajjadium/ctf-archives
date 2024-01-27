package main

import (
	"encoding/binary"
	"encoding/hex"
	"flag"
	"io"
	"log"

	"github.com/songgao/water"
	"golang.org/x/net/websocket"
)

var (
	url string
	hexdump bool
)

func init() {
	flag.StringVar(&url, "url", "", "WebSocket URL in form of wss://47.88.103.9:1337/nic/XXXXXXXXXXXX")
	flag.BoolVar(&hexdump, "hexdump", false, "dump traffic as hex")
}

func main() {
	flag.Parse()

	// open tap interface
	iface, err := water.New(water.Config{
		DeviceType: water.TAP,
		PlatformSpecificParams: platformSpecificParams,
	})
	if err != nil {
		log.Fatal(err)
	}
	tapFixup()

	// dial websocket
	ws, err := websocket.Dial(url, "", "https://47.88.103.9:1337")
	if err != nil {
		log.Fatal(err)
	}
	ws.PayloadType = websocket.BinaryFrame

	log.Print("start forwarding wss <=> tap");

	// wss->tap
	go func() {
		var buf [1518]byte
		for {
			_, err := io.ReadFull(ws, buf[:4])
			if err != nil {
				log.Fatal(err)
			}
			n := binary.BigEndian.Uint32(buf[:4])
			if n > 1518 {
				_, err = io.CopyN(io.Discard, ws, int64(n))
				if err != nil {
					log.Fatal(err)
				}
				continue
			}
			_, err = io.ReadFull(ws, buf[:n])
			if err != nil {
				log.Fatal(err)
			}
			if hexdump {
				log.Printf("wss->tap: (%d bytes)\n%s", n, hex.Dump(buf[:n]))
			}
			_, err = iface.Write(buf[:n])
			if err != nil {
				log.Fatal(err)
			}
		}
	}()

	// tap -> wss
	go func() {
		var buf [4+1518]byte
		for {
			n, err := iface.Read(buf[4:])
			if err != nil {
				log.Fatal(err)
			}
			binary.BigEndian.PutUint32(buf[:4], uint32(n))
			if hexdump {
				log.Printf("tap->wss: (%d bytes)\n%s", n, hex.Dump(buf[4:4+n]))
			}
			_, err = ws.Write(buf[:4+n])
			if err != nil {
				log.Fatal(err)
			}
		}
	}()

	select {}
}
