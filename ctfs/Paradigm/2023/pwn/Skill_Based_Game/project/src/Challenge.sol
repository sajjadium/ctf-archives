// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract Challenge {
    address public immutable BLACKJACK;

    constructor(address blackjack) {
        BLACKJACK = blackjack;
    }

    function isSolved() external view returns (bool) {
        return BLACKJACK.balance == 0;
    }
}
