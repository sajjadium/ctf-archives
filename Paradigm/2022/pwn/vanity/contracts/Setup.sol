// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.7.6;

import "./Challenge.sol";

contract Setup {
    Challenge public immutable challenge;

    constructor() {
        challenge = new Challenge();
    }

    function isSolved() external view returns (bool) {
        return challenge.bestScore() >= 16;
    }
}
