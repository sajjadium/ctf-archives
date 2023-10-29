// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract Challenge {
    IERC20 private immutable WETH = IERC20(0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2);

    address public immutable dvm;

    constructor(address dvm_) {
        dvm = dvm_;
    }

    function isSolved() external view returns (bool) {
        return WETH.balanceOf(dvm) == 0;
    }
}
