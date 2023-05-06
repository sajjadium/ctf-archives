pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "hardhat/console.sol";

contract SecureSlot {
    struct Bet {
        uint block;
        uint amount;
        bytes32 input;
        address player;
    }

    event BetAccepted(uint index);
    event AmountWon(uint amount);

    ERC20 chips;
    Bet[] public bets;

    constructor(ERC20 _chips) {
        chips = _chips;
    }

    modifier noContracts() {
        require(msg.sender == tx.origin, "Only humans are allowed into the KAsino");
        _;
    }

    function play(uint amount, bytes32 input) public noContracts {
        require(chips.allowance(msg.sender, address(this)) >= amount, "Can't access chips");
        require(amount >= 10, "Sorry, high-rollers only");

        chips.transferFrom(msg.sender, address(this), amount);
        bets.push(Bet(block.number, amount, input, msg.sender));

        emit BetAccepted(bets.length - 1);
    }

    function claim(uint index) public noContracts {
        require(bets.length > index, "Invalid bet");
        Bet memory bet = bets[index];

        require(bet.player == msg.sender, "Not your bet");
        require(block.number > bet.block, "Still spinning");
        require(block.number - bet.block < 300, "Too slow");

        bytes32 a = bytes20(bet.player) ^ bytes32(0);
        uint256 c = uint256(blockhash(bet.block) ^ bet.input ^ a);
        uint256 b = chips.balanceOf(address(this));

        delete bets[index];

        uint256 w = 0;

        if (c <= b) {
            w = b - c;
        }

        chips.transfer(bet.player, w);
        emit AmountWon(w);
    }

    function cleanup(uint index) public {
        require(bets.length > index && block.number - bets[index].block > 300, "Invalid cleanup");

        delete bets[index];
    }
}
