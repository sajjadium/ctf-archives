// SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;

contract burgercoin {
    address public owner;
    mapping (address => uint) public balances;
    int public totalSupply;


    constructor() {
        owner = msg.sender;
        balances[owner] = 30;
        // only 10 burgercoin in circulation for now
        totalSupply = 10;
    }

    function purchaseBurger() public {
        require(balances[msg.sender] == 0, "You already claimed your burgercoin!");
        balances[msg.sender] = 1;
        totalSupply -= 1;
    }

    function giveBurger(address to) public {
        require(balances[msg.sender] >= 30, "You are not the burger joint owner");
        balances[to] += 1;
    }

    function transfer(address to, uint amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }

    function getBalance(address user) public view returns (uint) {
        return balances[user];
    }

    function transferBurgerjointOwnership(address newOwner) public {
        require(balances[msg.sender] >= 30, "You are not the burger joint owner");
        owner = newOwner;
    }

    function isSolved() public view returns (bool) {
        return balances[owner] == 0;
    }
}
