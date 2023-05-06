// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.15;

contract Guesser {

    bool public solved = false;

    function _getDiceRoll() internal pure returns (uint256) {   
        return 1;                                                   
    }
    
    function solve(uint256 guess) public {
        require(guess == _getDiceRoll());
        solved = true;
    }
}