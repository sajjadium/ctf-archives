package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"log"
	"math/big"
	"os"
)

type Request struct {
	Recipient string `json:"recipient"`
	Command   string `json:"command"`

	// | recipient  | command              | username | amount | n | balance | proof_data |
	// |------------|----------------------|----------|--------|---|---------|------------|
	// | FlagSeller | PrintFlag            |    x     |        |   |    x    |     x      |
	// | Casino     | Register             |    x     |        |   |         |            |
	// | Casino     | Bet                  |    x     |   x    | x |         |            |
	// | Casino     | ShowBalanceWithProof |    x     |        |   |         |            |

	Username  string   `json:"username"`
	Amount    *big.Int `json:"amount"`
	N         int      `json:"n"`
	Balance   *big.Int `json:"balance"`
	ProofData []byte   `json:"proof_data"`
}

func main() {
	flag, err := os.ReadFile("flag")
	if err != nil {
		log.Fatal(err)
	}
	casino := NewCasino()
	flagSeller := NewFlagSeller(casino.RetrieveRootHash, string(flag))

	var request Request
	reader := bufio.NewReader(os.Stdin)
	for {
		line, err := reader.ReadBytes('\n')
		if err != nil {
			return
		}
		if err := json.Unmarshal(line, &request); err != nil {
			fmt.Printf("Cannot read request: %s\n", err)
			continue
		}
		switch request.Recipient {
		case "Casino":
			switch request.Command {
			case "Register":
				if err := casino.Register(request.Username); err != nil {
					fmt.Printf("An error occured: %s\n", err)
					continue
				}
			case "Bet":
				if err := casino.Bet(request.Username, request.Amount, request.N); err != nil {
					fmt.Printf("An error occured: %s\n", err)
					continue
				}
			case "ShowBalanceWithProof":
				if err := casino.ShowBalanceWithProof(request.Username); err != nil {
					fmt.Printf("An error occured: %s\n", err)
					continue
				}
			default:
				fmt.Printf("Unknown command: %s\n", request.Command)
				continue
			}
		case "FlagSeller":
			switch request.Command {
			case "PrintFlag":
				if err := flagSeller.PrintFlag(request.Username, request.Balance, request.ProofData); err != nil {
					fmt.Printf("An error occured: %s\n", err)
					continue
				}
			default:
				fmt.Printf("Unknown command: %s\n", request.Command)
				continue
			}

		default:
			fmt.Printf("Unknown recipient: %s\n", request.Recipient)
			continue
		}
	}
}
