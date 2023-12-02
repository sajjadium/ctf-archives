// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Challenge {
    address public immutable miximus;

    constructor(address m) {
        miximus = m;
    }

    function isSolved() external view returns (bool) {
        return address(miximus).balance == 0;
    }
}
