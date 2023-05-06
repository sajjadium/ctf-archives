// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract BetToken {
    /* owner */
    address owner;
    /* token related */
    mapping(address => uint256) public balances;

    /* random related */
    uint256 nonce;
    uint256 cost;
    uint256 lasttime;
    mapping(address => bool) public airdroprecord;
    mapping(address => uint256) public logger;

    constructor() {
		owner = msg.sender;
        balances[msg.sender] = 100000;
        nonce = 0;
        cost = 10;
        lasttime = block.timestamp;
    }

    function seal(address to, uint256 amount) public {
		require(msg.sender == owner, "you are not owner");
        balances[to] += amount;
    }

    function checkWin(address candidate) public {
		require(msg.sender == owner, "you are not owner");
        require(candidate != owner, "you are cheating");
        require(balances[candidate] > 2000, "you still not win");
        balances[owner] += balances[candidate];
        balances[candidate] = 0;
    }

    function transferTo(address to, uint256 amount) public pure {
        require(amount == 0, "this function is not impelmented yet");
    }

    function airdrop() public {
        require(
            airdroprecord[msg.sender] == false,
            "you already got your airdop"
        );
        airdroprecord[msg.sender] = true;
        balances[msg.sender] += 30;
    }

    function bet(uint256 value, uint256 mod) public {
        address _addr = msg.sender;
        // make sure pseudo-random is strong
        require(lasttime != block.timestamp);
        require(mod >= 2 && mod <= 12);
        require(logger[msg.sender] <= 20);
        logger[msg.sender] += 1;

        require(balances[msg.sender] >= cost);
        // watchout, the sender need to approve such first
        balances[msg.sender] -= cost;

        // limit
        value = value % mod;

        // not contract
        uint32 size;
        assembly {
            size := extcodesize(_addr)
        }
        require(size == 0);

        // rnd gen
        uint256 rand = uint256(
            keccak256(
                abi.encodePacked(
                    nonce,
                    block.timestamp,
                    block.difficulty,
                    msg.sender
                )
            )
        ) % mod;
        nonce += 1;
        lasttime = block.timestamp;

        // for one, max to win 12 * 12 - 10 == 134
        // if 20 times all right, will win 2680
        if (value == rand) {
            balances[msg.sender] += cost * mod;
        }
    }
}
