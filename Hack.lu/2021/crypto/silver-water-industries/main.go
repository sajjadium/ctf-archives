package main

import (
	"bufio"
	"crypto/rand"
	"fmt"
	"math"
	"math/big"
	"os"
)

func genN() *big.Int {
	var p *big.Int
	var q *big.Int
	var err error

	for {
		p, err = rand.Prime(rand.Reader, 64)
		if err != nil {
			panic(err)
		}
		res := new(big.Int)
		if res.Mod(p, big.NewInt(4)); res.Cmp(big.NewInt(1)) == 0 {
			break
		}
	}

	for {
		q, err = rand.Prime(rand.Reader, 64)
		if err != nil {
			panic(err)
		}
		res := new(big.Int)
		if res.Mod(q, big.NewInt(4)); res.Cmp(big.NewInt(3)) == 0 {
			break
		}
	}

	N := new(big.Int)
	N.Mul(p, q)
	return N
}

func genX(N *big.Int) *big.Int {
	for {
		x, err := rand.Int(rand.Reader, N)
		if err != nil {
			panic(err)
		}
		g := new(big.Int)
		g.GCD(nil, nil, x, N)
		if g.Cmp(big.NewInt(1)) == 0 {
			return x
		}
	}
}

func encryptByte(b uint8, N *big.Int) []*big.Int {
	z := big.NewInt(-1)
	enc := make([]*big.Int, 8)
	for i := 0; i < 8; i++ {
		bit := b & uint8(math.Pow(2, float64(7-i)))
		x := genX(N)
		x.Exp(x, big.NewInt(2), N)
		if bit != 0 {
			x.Mul(x, z)
			x.Mod(x, N)
		}
		enc[i] = x
	}
	return enc
}

func generateRandomString(n int) string {
	const letters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-"
	ret := make([]byte, n)
	for i := 0; i < n; i++ {
		num, err := rand.Int(rand.Reader, big.NewInt(int64(len(letters))))
		if err != nil {
			panic(err)
		}
		ret[i] = letters[num.Int64()]
	}

	return string(ret)
}

func main() {
	N := genN()

	token := []byte(generateRandomString(20))

	fmt.Println(N)
	for _, b := range token {
		fmt.Println(encryptByte(uint8(b), N))
	}
	fmt.Println("")

	reader := bufio.NewReader(os.Stdin)

	input, err := reader.ReadString('\n')
	if err != nil {
		panic(err)
	}
	input = input[:len(input)-1]

	if string(token) == input {
		fmt.Println("flag{<YOUR_FLAG_HERE>}")
	}
}
