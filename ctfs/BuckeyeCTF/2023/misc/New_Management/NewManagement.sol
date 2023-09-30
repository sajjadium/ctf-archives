// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;


contract NewManagement {
    mapping(address => uint) balances;
    string currentMessage;
    address owner;

    event GetFlag(bytes16 flag);
    event Registered(address indexed);
    event IncreasedBalance(address indexed, uint);
    event DecreaseBalance(address indexed, uint);
    event Transfer(address indexed, address indexed, uint);
    event SetMessage(address indexed, string);

    constructor() {
        owner = msg.sender;
    }

    function increaseBalance(address addr, uint amount) public {
        require(owner == msg.sender);

        balances[addr] += amount;
        emit IncreasedBalance(addr, amount);
    }

    function decreaseBalance(address addr, uint amount) public {
        require(owner == msg.sender);

        balances[addr] -= amount;
        emit DecreaseBalance(addr, amount);
    }

    function clearMessage() public {
        require(owner == msg.sender);

        currentMessage = "";
    }

    function register() public {
        require(balances[msg.sender] == 0);

        balances[msg.sender] = 100;
        emit Registered(msg.sender);
    }

    function transfer(address to, uint amount) public {
        require(balances[msg.sender] >= amount);

        balances[msg.sender] -= amount;
        balances[to] += amount;
        emit Transfer(msg.sender, to, amount);
    }

    function setMessage(string calldata message) public {
        require(balances[msg.sender] == 100);

        currentMessage = message;
        balances[msg.sender] -= 100;
        emit SetMessage(msg.sender, message);
    }

    function transferOwnership(address to) public {
        owner = to;
    }

    function burn() public {
        balances[msg.sender] = 0;
    }

    function burn(uint amount) public {
        balances[msg.sender] -= amount;
    }

    function getFlag(bytes16 flag) public {
        require(balances[msg.sender] > 1000);

        emit GetFlag(flag);
    }
}