// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract Setup {
    bool private solved;

    constructor() payable {
    }

    function solve(bytes calldata secret) public {
        require(keccak256(secret) == keccak256(bytes("CJ_INTERNATIONAL_2024-CHOVID99")), "Wrong password");
        solved = true;
    }

    function isSolved() external view returns (bool) {
        return solved;
    }
}