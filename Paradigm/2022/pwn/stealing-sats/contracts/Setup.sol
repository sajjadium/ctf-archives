// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.16;

interface ERC20Like {
    function balanceOf(address) external view returns (uint);
}

contract Setup {
    ERC20Like public immutable WBTC = ERC20Like(0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599);
    address public immutable TARGET = 0x8D90113A1e286a5aB3e496fbD1853F265e5913c6;

    uint public immutable INITIAL_BALANCE;

    constructor() {
        INITIAL_BALANCE = WBTC.balanceOf(TARGET);
    }

    function isSolved() external view returns (bool) {
        return INITIAL_BALANCE - WBTC.balanceOf(TARGET) >= 128;
    }
}