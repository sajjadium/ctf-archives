package main

import (
	"fmt"
	"github.com/cosmos/iavl"
	iavlproto "github.com/cosmos/iavl/proto"
	"github.com/golang/protobuf/proto"
	"math/big"
)

type FlagSeller struct {
	dbRootRetriever func() []byte
	flag            string
}

func NewFlagSeller(dbRootRetriever func() []byte, flag string) *FlagSeller {
	return &FlagSeller{
		dbRootRetriever: dbRootRetriever,
		flag:            flag,
	}
}

func (fs *FlagSeller) PrintFlag(usename string, balance *big.Int, proofData []byte) error {
	var pbProof iavlproto.RangeProof
	if err := proto.Unmarshal(proofData, &pbProof); err != nil {
		return fmt.Errorf("bad proof format: %w", err)
	}
	proof, err := iavl.RangeProofFromProto(&pbProof)
	if err != nil {
		return fmt.Errorf("bad proof format: %w", err)
	}
	if err := proof.Verify(fs.dbRootRetriever()); err != nil {
		return fmt.Errorf("proof verification failed: %w", err)
	}
	if err := proof.VerifyItem([]byte(usename), balance.Bytes()); err != nil {
		return fmt.Errorf("proof verification failed: %w", err)
	}

	l := balance.BitLen() / 8
	dot3 := "..."
	if l >= len(fs.flag) {
		l = len(fs.flag)
		dot3 = ""
	}
	fmt.Printf("Your flag is: %s%s\n", fs.flag[:l], dot3)
	return nil
}
