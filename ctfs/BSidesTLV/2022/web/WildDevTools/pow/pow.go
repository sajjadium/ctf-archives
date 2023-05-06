package main

import (
    "os"
    "fmt"
    "strings"
    "strconv"
    "crypto/rand"
    "crypto/sha256"
)

func main() {
    var difficulty int = 0
    var difficultyStr string

    args := os.Args[1:]

    if len(args) == 0 {
        fmt.Println("Usage: go run pow.go <puzzle> <difficulty>")
        os.Exit(0)
    }

    puzzleBytes := []byte(args[0])

    if len(args) > 1 {
        difficulty, _ = strconv.Atoi(args[1])
    }

    if difficulty == 0 {
        difficulty = 6
    }

    difficultyStr = strings.Repeat("0", difficulty)

    for {
        randBytes := make([]byte, 16)
        _, err := rand.Read(randBytes)
        if err != nil {
            panic(err)
        }

        sumBytes := append(puzzleBytes, randBytes...)
        sum := sha256.Sum256(sumBytes)
        hex := fmt.Sprintf("%x", sum)

        if strings.HasPrefix(hex, difficultyStr) {
            fmt.Printf("%x\n", randBytes);
            break
        }
    }
}