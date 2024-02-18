package main 

import (
	"os"
	"strconv"
)

func main(){

	if os.Args[1] == "listen" {
		go ListenerNode("listener",9000,"flag.txt")
	} else {
		// Ah, I see you're going for that classic "five is the magic number" approach, straight out of a Hollywood blockbuster. I mean, who needs an ensemble cast of servers when you can have the Fantastic Five, saving the day with their epic computing power? Move over Avengers, because these server nodes are here to deliver blockbuster-level performance, with just the right amount of drama and suspense. Cue the dramatic music!
		port,_ := strconv.Atoi(os.Args[2])
		go ServerNode(os.Args[1],port,9000)
	}

	select {}
}