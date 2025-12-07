// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.30;

contract Blockchain101 {
    bool private chall_solved;

    constructor() payable {}

    function solveChall(string memory argument) public {
        if (keccak256(abi.encodePacked(argument)) == keccak256(abi.encodePacked("hackerschallenge"))) {
            chall_solved = true;
        }
        else {
            revert("Incorrect argument");
        }
    }

    function isSolved() external view returns (bool) {
        return chall_solved;
    }
}
