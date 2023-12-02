// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

interface IERC20 {
    function balanceOf(address account) external view returns (uint256);
}

contract Challenge {
    IERC20 stETH = IERC20(0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84);

    constructor(address) {}

    function isSolved() public view returns (bool) {
        return stETH.balanceOf(address(this)) >= 260000 ether;
    }
}
