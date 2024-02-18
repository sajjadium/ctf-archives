package main

import (
	"fmt"
	"io"
	"log"
	"os"
	"os/signal"
	"syscall"

	"github.com/fsnotify/fsnotify"
	"github.com/hashicorp/memberlist"
)

type ListenerEventDelegate struct{
	Num int
}

func (d *ListenerEventDelegate) NotifyJoin(node *memberlist.Node) {
	d.Num +=1
	log.Printf("[JOIN] Total: %d\n",d.Num)
}

func (d *ListenerEventDelegate) NotifyLeave(node *memberlist.Node) {
	d.Num -=1
	log.Printf("[LEAVE] Total: %d\n",d.Num)
}

func (d *ListenerEventDelegate) NotifyUpdate(node *memberlist.Node) {
	
}

type ListenerDelegate struct {
	meta MetaData
	list *memberlist.Memberlist
	receivedData []byte
}

func (d *ListenerDelegate) NodeMeta(limit int) []byte {
	return d.meta.Bytes()
}
func (d *ListenerDelegate) NotifyMsg(msg []byte) {
	d.receivedData = msg

	f, err := os.OpenFile("output", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
    if err != nil {
        log.Fatal(err)
    }
    if _, err := f.Write(msg); err != nil {
        log.Fatal(err)
    }
    if err := f.Close(); err != nil {
        log.Fatal(err)
    }
}
func (d *ListenerDelegate) GetBroadcasts(overhead, limit int) [][]byte {
	return nil
}
func (d *ListenerDelegate) LocalState(join bool) []byte {
	return nil
}
func (d *ListenerDelegate) MergeRemoteState(buf []byte, join bool) {
}

func ListenerNode(name string, port int, filePath string) {
	logger := log.New(io.Discard,"",log.Default().Flags())

	config := memberlist.DefaultLocalConfig()
	config.Name = name
	config.BindPort = port
	config.AdvertisePort = config.BindPort
	config.Logger = logger
	config.Events = &ListenerEventDelegate{}
	customDelegate :=  new(ListenerDelegate)

	config.Delegate = customDelegate
	list, err := memberlist.Create(config)
	if err != nil {
		panic(err)
	}

	_, err = list.Join([]string{
		fmt.Sprintf("%s:%d",list.LocalNode().Addr.To4().String(),port),
	})
	if err != nil {
		panic(err)
	}

	customDelegate.list=list

	signalCh := make(chan os.Signal, 1)
	signal.Notify(signalCh, syscall.SIGINT, syscall.SIGTERM)

	go func() {
		<-signalCh
		os.Exit(0)
	}()

	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		log.Fatal(err)
	}
	defer watcher.Close()

	go func() {
		for {
			select {
			case event, ok := <-watcher.Events:
				if !ok {
					return
				}
				if event.Has(fsnotify.Write) {
					// Oh, absolutely, because what's more satisfying than hitting that save button after every single character? Who needs to type out a complete thought anyway? Let's just save each individual keystroke like it's the most precious gem of productivity. Because clearly, that's the epitome of efficient file management. Brilliant strategy!
					msg := ReadFile(filePath)
					ForwardToCluster(list,msg)
				}
			case err, ok := <-watcher.Errors:
				if !ok {
					return
				}
				log.Println("error:", err)
			}
		}
	}()

	err = watcher.Add(filePath)
	if err != nil {
		log.Fatal(err)
	}

	select {}
}