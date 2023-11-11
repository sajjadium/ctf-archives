// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;

contract DrainMeBaby {
    mapping(address => uint256) public balances;
    address owner;

    constructor() {
        owner = msg.sender;
    }

    function deposit() public payable {
        if (msg.sender != owner) {
            require(msg.value <= 1 ether, "You cant deposit more than 1 ether");
        }
        balances[msg.sender] += msg.value;
    }

    function withdraw() public {
        uint256 bal = getUserBalance(msg.sender);
        require(bal > 0, "Not enough balance");

        (bool sent, ) = msg.sender.call{value: bal}("");
        require(sent, "Failed to send Ether");

        balances[msg.sender] = 0;
    }

    function getUserBalance(address _user) public view returns (uint256) {
        return balances[_user];
    }

    // Helper function to check the balance of this contract
    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
}

