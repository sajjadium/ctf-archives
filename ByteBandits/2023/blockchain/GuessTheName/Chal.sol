// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

interface Checker {
    function isCorrectGuess(uint256) external returns (bool);
}

contract Challenge {
    bool public win;
    uint256 public guess;

    function makeAGuess(uint256 _guess) public {
        Checker checker = Checker(msg.sender);

        if (!checker.isCorrectGuess(_guess)) {
            guess = _guess;
            win = checker.isCorrectGuess(guess);
        }
    }
}
