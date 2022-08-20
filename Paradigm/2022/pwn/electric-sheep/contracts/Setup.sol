// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.16;

interface ERC20Like {
    function balanceOf(address) external view returns (uint);
}

contract Setup {
    ERC20Like public immutable DREAMERS = ERC20Like(0x1C4d5CA50419f94fc952a20DdDCDC4182Ef77cdF);

    function isSolved() external view returns (bool) {
        return DREAMERS.balanceOf(address(this)) > 16 ether;
    }
}