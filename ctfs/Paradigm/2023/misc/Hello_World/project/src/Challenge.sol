// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

contract Challenge {
    address public immutable TARGET = 0x00000000219ab540356cBB839Cbe05303d7705Fa;

    uint256 public immutable STARTING_BALANCE;

    constructor() {
        STARTING_BALANCE = address(TARGET).balance;
    }

    function isSolved() external view returns (bool) {
        return TARGET.balance > STARTING_BALANCE + 13.37 ether;
    }
}
