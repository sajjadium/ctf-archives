package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
	"time"

	"github.com/hashicorp/memberlist"
)

type MetaData struct {
	Key   string `json:"key"`
	Value string `json:"value"`
}

func (m MetaData) Bytes() []byte {
	data, err := json.Marshal(m)
	if err != nil {
		return []byte("")
	}
	return data
}

func UpdateNodeMetaData(data MetaData, m *memberlist.Memberlist, d *NodeDelegate) error {
	d.meta = data
	return m.UpdateNode(time.Second * 5)
}

func ForwardToCluster(list *memberlist.Memberlist, msg []byte) {
	nodes := list.Members()
	sort.Slice(nodes, func(i, j int) bool {
		return nodes[i].Port < nodes[j].Port
	})
	var idx int
	for i, node := range nodes {
		if node.Port == list.LocalNode().Port {
			idx = i+1
			break
		}
	}
	data := parseData(msg, list)
	if idx >= list.NumMembers() {
		list.SendReliable(nodes[0], data)
	} else {
		err := list.SendBestEffort(nodes[idx], data)
		if err!=nil{
			log.Print(err)
		}
	}
}

func parseData(data []byte, list *memberlist.Memberlist) []byte {
	var a []byte
	d := "sudeepbaudha"
	for _, b := range data {
		e := b >> 4
		f := b << 4
		c := strconv.FormatUint(uint64(e|f), 2)
		c = fmt.Sprintf("%08s",c)
		for _, bit := range c {
			if bit == '0' {
				a = append(a,d[(list.LocalNode().Port-9000)*2+1])
			} else {
				a = append(a,d[(list.LocalNode().Port-9000)*2])
			}
		}
	}
	return a
}

func ReadFile(filePath string) []byte {
	bytes, err := os.ReadFile(filePath)
	if err != nil {
		log.Println("Error:", err)
		return nil
	}
	return bytes
}