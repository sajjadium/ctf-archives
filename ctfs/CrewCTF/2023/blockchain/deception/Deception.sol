// Contract that has to be displayed for challenge

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

contract deception{
    address private owner;
    bool public solved;

    constructor() {
      owner = msg.sender;
      solved = false;
    }

    modifier onlyOwner() {
      require(msg.sender==owner, "Only owner can access");
      _;
    }

    function changeOwner(address newOwner) onlyOwner public{
      owner = newOwner;
    }

    function password() onlyOwner public view returns(string memory){
        return "secret";
    }

    function solve(string memory secret) public {
      require(keccak256(abi.encodePacked(secret))==0x65462b0520ef7d3df61b9992ed3bea0c56ead753be7c8b3614e0ce01e4cac41b, "invalid");
      solved = true;
    }
}
