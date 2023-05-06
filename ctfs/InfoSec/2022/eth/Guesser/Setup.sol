// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.15;

import "./Guesser.sol";

contract Setup {

    Guesser public guesser;

    constructor() {
        guesser = new Guesser();
    }

    function isSolved() public view returns (bool) {
        return guesser.solved();
    }
}