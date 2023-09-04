// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract EightFiveFourFive {
    string private use_this;
    bool public you_solved_it = false;

    constructor(string memory some_string) {
        use_this = some_string;
    }

    function readTheStringHere() external view returns (string memory) {
        return use_this;
    }

    function solve_the_challenge(string memory answer) external {
        you_solved_it = keccak256(bytes(answer)) == keccak256(bytes(use_this));
    }

    function isSolved() external view returns (bool) {
        return you_solved_it;
    }
}
