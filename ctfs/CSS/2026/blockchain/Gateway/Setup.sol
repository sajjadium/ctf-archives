// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import {Gate} from "./Gate.sol";

contract Setup {
    Gate public gate;

    constructor() payable {
        gate = (new Gate){value: msg.value}();
    }

    function isSolved() external view returns (bool) {
        return gate.solved();
    }
}
