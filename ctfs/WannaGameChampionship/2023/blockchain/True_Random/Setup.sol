// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;

import "./LuckyWheel.sol";

contract Setup {
    LuckyWheel public immutable luckyWheel;

    constructor() {
        luckyWheel = new LuckyWheel();
    }

    function isSolved() external view returns (bool) {
        return luckyWheel.closed() == 1;
    }
}
