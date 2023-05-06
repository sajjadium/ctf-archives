// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.18;

import "./EVMVM.sol";

contract Setup {
    EVMVM public immutable metametaverse = new EVMVM();
    bool private solved = false;

    function solve() external {
        assert(msg.sender == address(metametaverse));
        solved = true;
    }

    function isSolved() external view returns (bool) {
        return solved;
    }
}
