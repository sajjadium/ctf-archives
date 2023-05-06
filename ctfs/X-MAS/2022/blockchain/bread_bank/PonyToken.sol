// SPDX-License-Identifier: Unlicensed

pragma solidity 0.8.17;

import "./ERC20.sol";

contract PonyToken is ERC20("Pony", "PNY") {

    constructor(uint256 _amount) {
        _mint(msg.sender, _amount);
    }
}