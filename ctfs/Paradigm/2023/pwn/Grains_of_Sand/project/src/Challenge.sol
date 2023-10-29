// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract Challenge {
    IERC20 private immutable TOKEN = IERC20(0xC937f5027D47250Fa2Df8CbF21F6F88E98817845);

    address private immutable TOKENSTORE = 0x1cE7AE555139c5EF5A57CC8d814a867ee6Ee33D8;

    uint256 private immutable INITIAL_BALANCE;

    constructor() {
        INITIAL_BALANCE = TOKEN.balanceOf(TOKENSTORE);
    }

    function isSolved() external view returns (bool) {
        return INITIAL_BALANCE - TOKEN.balanceOf(TOKENSTORE) >= 11111e8;
    }
}
