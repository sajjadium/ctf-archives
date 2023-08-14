package main

import (
	"crypto/elliptic"
	cryptorand "crypto/rand"
	"crypto/sha256"
	"encoding/base64"
	"fmt"
	"log"
	"math"
	"math/big"
	"math/rand"
	"os"
)

func randInt64() int64 {
	n, err := cryptorand.Int(cryptorand.Reader, big.NewInt(math.MaxInt64))
	if err != nil {
		panic(err)
	}
	return n.Int64()
}

func encrypt(data, priv []byte) string {
	res := make([]byte, 0)
	st := sha256.Sum256(priv)
	for i, b := range data {
		res = append(res, b^st[i])
	}
	return base64.StdEncoding.EncodeToString(res)
}

func decrypt(enc string, priv []byte) string {
	res := make([]byte, 0)
	data, _ := base64.StdEncoding.DecodeString(enc)
	st := sha256.Sum256(priv)
	for i, b := range data {
		res = append(res, b^st[i])
	}
	return string(res)
}

func main() {
	flag := os.Getenv("FLAG")

	curve := elliptic.P256()
	priv, _, _, err := elliptic.GenerateKey(curve, cryptorand.Reader)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("enc_flag = %q\n", encrypt([]byte(flag), priv))

	rand.Seed(randInt64())

	for i := int64(0); i < randInt64(); i++ {
		rand.Uint64()
	}

	for i := 0; i <= 607; i++ {
		msg := fmt.Sprintf("msg_%d", i)
		hash := sha256.Sum256([]byte(msg))
		h := new(big.Int).SetBytes(hash[:])

		r, s := Sign(curve, rand.Uint64(), priv, h)

		fmt.Printf("h[%[1]d] = %[2]s\nr[%[1]d] = %[3]s\ns[%[1]d] = %[4]s\n", i, h, r, s)
	}
}

func Sign(curve elliptic.Curve, nonce uint64, priv []byte, h *big.Int) (*big.Int, *big.Int) {
	r := new(big.Int)
	s := new(big.Int)
	d := new(big.Int).SetBytes(priv)
	k := new(big.Int).SetUint64(nonce)

	x, _ := curve.ScalarBaseMult(k.Bytes())
	r.Mod(x, curve.Params().P)

	if r.Sign() == 0 {
		panic("bad nonce")
	}

	s.Mul(r, d)
	s.Mod(s, curve.Params().N)
	s.Add(s, h)
	s.Mod(s, curve.Params().N)
	k.ModInverse(k, curve.Params().N)
	s.Mul(s, k)
	s.Mod(s, curve.Params().N)

	return r, s
}
