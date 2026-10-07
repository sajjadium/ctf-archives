// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import {Lottery} from "./Lottery.sol";

contract Setup {
    Lottery public lottery;

    constructor() {
        lottery = new Lottery();
    }

    function isSolved() external view returns (bool) {
        return lottery.winner() != address(0);
    }
}
