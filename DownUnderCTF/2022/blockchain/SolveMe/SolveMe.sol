// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

/**
 * @title SolveMe
 * @author BlueAlder duc.tf
 */
contract SolveMe {
    bool public isSolved = false;

    function solveChallenge() external {
        isSolved = true;
    }
   
}