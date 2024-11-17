// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Vault {
    string private password; 
    // setting owner to your wallet address will allow you to claim the flag on challs.crate.nu:50004
    address public owner;

    constructor(string memory pass) {
        password = pass;
        owner = msg.sender;
    }

    function changeOwner(string memory pass) public payable{
        require(msg.value >= 0.1 ether, "Must send at least 0.1 ether to changeOwner");
        require(keccak256(abi.encodePacked(password)) == keccak256(abi.encodePacked(pass)), "wrong password");
        owner = msg.sender;
    }
}
