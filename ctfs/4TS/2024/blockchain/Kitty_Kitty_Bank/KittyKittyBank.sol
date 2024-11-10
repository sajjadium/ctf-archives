pragma solidity ^0.6.0;

contract KittyKittyBank {
    mapping(address => uint) public kittykittycats;
    
    constructor() public payable { }

    function sendKitties() public payable {
        kittykittycats[msg.sender] += msg.value;
    }

    function pullbackKitties() public {
        uint kittens = kittykittycats[msg.sender];

        msg.sender.call.value(kittens)("");

        kittykittycats[msg.sender] = 0;
    }

    function getBalance() public view returns (uint) {
        return address(this).balance;
    }
}
