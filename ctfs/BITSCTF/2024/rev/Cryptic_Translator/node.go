package main

import (
	"io"
	"log"
	"fmt"

	"github.com/hashicorp/memberlist"
)



type NodeEventDelegate struct {
	Num int
}

func (d *NodeEventDelegate) NotifyJoin(node *memberlist.Node) {
	d.Num += 1
}

func (d *NodeEventDelegate) NotifyLeave(node *memberlist.Node) {
	d.Num -= 1
}

func (d *NodeEventDelegate) NotifyUpdate(node *memberlist.Node) {

}

type NodeDelegate struct {
	meta MetaData
	list *memberlist.Memberlist
}

func (d *NodeDelegate) NodeMeta(limit int) []byte {
	return d.meta.Bytes()
}
func (d *NodeDelegate) NotifyMsg(msg []byte) {
	ForwardToCluster(d.list, msg)
}
func (d *NodeDelegate) GetBroadcasts(overhead, limit int) [][]byte {
	return nil
}
func (d *NodeDelegate) LocalState(join bool) []byte {
	return nil
}
func (d *NodeDelegate) MergeRemoteState(buf []byte, join bool) {
}

func ServerNode(name string, port int , listenerPort int) {

	logger := log.New(io.Discard, "", log.Default().Flags())

	config := memberlist.DefaultLocalConfig()
	config.Name = name
	config.BindPort = port
	config.AdvertisePort = config.BindPort
	config.Logger = logger
	config.Events = &NodeEventDelegate{}
	customDelegate := new(NodeDelegate)

	config.Delegate = customDelegate
	list, err := memberlist.Create(config)
	if err != nil {
		panic(err)
	}

	_, err = list.Join([]string{
		fmt.Sprintf("%s:%d",list.LocalNode().Addr.To4().String(),listenerPort),
	})
	if err != nil {
		panic(err)
	}

	customDelegate.list = list

	select {}
}
