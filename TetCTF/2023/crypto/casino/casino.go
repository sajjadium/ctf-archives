package main

import (
	cryptorand "crypto/rand"
	"encoding/base64"
	"encoding/binary"
	"errors"
	"fmt"
	"github.com/cosmos/iavl"
	db "github.com/tendermint/tm-db"
	"log"
	"math/big"
	"math/rand"
)

type Casino struct {
	tree        *iavl.MutableTree
	numAccounts int
}

func NewCasino() *Casino {
	tree, err := iavl.NewMutableTree(db.NewMemDB(), 128, true)
	if err != nil {
		log.Fatal(err)
	}
	tmp := make([]byte, 8)
	if _, err = cryptorand.Read(tmp); err != nil {
		log.Fatal(err)
	}
	rand.Seed(int64(binary.LittleEndian.Uint64(tmp)))
	return &Casino{
		tree:        tree,
		numAccounts: 0,
	}
}

func (c *Casino) getBalance(username string) (*big.Int, error) {
	value, err := c.tree.Get([]byte(username))
	if err != nil {
		log.Fatal(err)
	}
	if value == nil {
		return nil, errors.New("player-not-exist")
	}
	return new(big.Int).SetBytes(value), nil
}

func (c *Casino) setBalance(username string, value *big.Int) {
	_, err := c.tree.Set([]byte(username), value.Bytes())
	if err != nil {
		log.Fatal(err)
	}
	_, _, err = c.tree.SaveVersion()
	if err != nil {
		log.Fatal(err)
	}
}

const MaxPlayers = 100
const InitialBalance = 2023

func (c *Casino) Register(username string) error {
	exist, err := c.tree.Has([]byte(username))
	if err != nil {
		log.Fatal(err)
	}
	if exist {
		return errors.New("player-exists")
	}
	if c.numAccounts >= MaxPlayers {
		return errors.New("max-players")
	}
	c.numAccounts += 1
	c.setBalance(username, big.NewInt(InitialBalance))
	fmt.Printf("Added user: %s.\n", username)
	return nil
}

func (c *Casino) Bet(username string, amount *big.Int, n int) error {
	currentBalance, err := c.getBalance(username)
	if err != nil {
		return err
	}
	if currentBalance.Cmp(amount) < 0 {
		return errors.New("insufficient-balance")
	}
	r := rand.Intn(2023)
	if r == n { // correct guess
		reward := new(big.Int).Mul(amount, big.NewInt(2022))
		currentBalance.Add(currentBalance, reward)
		c.setBalance(username, currentBalance)
		fmt.Printf("YOU WIN! Current balance: %d (+%d).\n", currentBalance, reward)
	} else {
		currentBalance.Sub(currentBalance, amount)
		c.setBalance(username, currentBalance)
		fmt.Printf("YOU LOSE (%d != %d)! Current balance: %d (-%d).\n", r, n, currentBalance, amount)
	}
	return nil
}

func (c *Casino) ShowBalanceWithProof(username string) error {
	value, proof, err := c.tree.GetWithProof([]byte(username))
	if err != nil {
		log.Fatal(err)
	}
	if value == nil {
		return errors.New("player-not-exist")
	}
	proofData, err := proof.ToProto().Marshal()
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("%d, %s\n", new(big.Int).SetBytes(value), base64.StdEncoding.EncodeToString(proofData))
	return nil
}

func (c *Casino) RetrieveRootHash() []byte {
	result, err := c.tree.Hash()
	if err != nil {
		log.Fatal(err)
	}
	return result
}
