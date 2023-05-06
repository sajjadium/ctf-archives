//SPDX-License-Identifier: Unlicensed
pragma solidity ^0.8.0;

import "./DUCoin.sol";
import "OpenZeppelin/openzeppelin-contracts@4.3.2/contracts/access/Ownable.sol";

contract Casino is Ownable {
    DUCoin public immutable ducoin;

    bool trialed = false;
    uint256 lastPlayed = 0;
    mapping(address => uint256) public balances;

    constructor(address token) {
        ducoin = DUCoin(token);
    }

    function deposit(uint256 amount) external {
        ducoin.transferFrom(msg.sender, address(this), amount);
        balances[msg.sender] += amount;
    }

    function withdraw(uint256 amount) external {
        require(balances[msg.sender] >= amount, "Insufficient balance!");
        ducoin.transfer(msg.sender, amount);
        balances[msg.sender] -= amount;
    }

    function _randomNumber() internal view returns(uint8) {
        uint256 ab = uint256(blockhash(block.number - 1));
        uint256 a = ab & 0xffffffff;
        uint256 b = (ab >> 32) & 0xffffffff;
        uint256 x = uint256(blockhash(block.number));
        return uint8((a * x + b) % 6);
    }

    function play(uint256 bet) external {
        require(balances[msg.sender] >= bet, "Insufficient balance!");
        require(block.number > lastPlayed, "Too fast!");
        lastPlayed = block.number;

        uint8 roll = _randomNumber();
        if(roll == 0) {
            balances[msg.sender] += bet;
        } else {
            balances[msg.sender] -= bet;
        }
    }

    function getTrialCoins() external {
        if(!trialed) {
            trialed = true;
            ducoin.transfer(msg.sender, 7);
        }
    }
}
