// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

contract Challenge {
    address public immutable BRIDGE;

    constructor(address bridge) {
        BRIDGE = bridge;
    }

    function isSolved() external view returns (bool) {
        return BRIDGE.balance == 0;
    }
}
