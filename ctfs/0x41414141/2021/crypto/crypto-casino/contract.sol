pragma solidity ^0.6.0;

contract casino {

    bytes32 private seed;
    mapping(address => uint) public consecutiveWins;

    constructor () public{
        seed = keccak256("satoshi nakmoto");
    }

    function bet(uint guess) public{
        uint num = uint(keccak256(abi.encodePacked(seed, block.number))) ^ 0x539;
        if (guess == num) {
            consecutiveWins[msg.sender] = consecutiveWins[msg.sender] + 1;
        }else {
            consecutiveWins[msg.sender] = 0;
        }
    }

    function done() public view returns (uint16[] memory) {
        if (consecutiveWins[msg.sender] > 1) {
            return [];
        }
    }

}
