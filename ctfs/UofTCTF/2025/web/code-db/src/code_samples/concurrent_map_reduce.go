package main

import (
    "fmt"
    "sync"
)

func main() {
    data := []int{1,2,3,4,5,6,7,8,9,10}
    var wg sync.WaitGroup
    squared := make([]int, len(data))
    wg.Add(len(data))
    for i, num := range data {
        go func(i, num int) {
            defer wg.Done()
            squared[i] = num * num
        }(i, num)
    }
    wg.Wait()

    sum := 0
    for _, num := range squared {
        sum += num
    }

    fmt.Println("Squared:", squared)
    fmt.Println("Sum:", sum)
}
