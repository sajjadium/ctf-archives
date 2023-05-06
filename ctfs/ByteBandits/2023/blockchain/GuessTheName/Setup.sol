// SPDX-License-Identifier: MIT

pragma solidity ^0.8.13;

import "./Chal.sol";

contract Setup {
    Challenge public immutable instance;

    constructor() payable {
        instance = new Challenge();
    }

    function isSolved() public view returns (bool) {
        return instance.win();
    }
}
