// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "../lib/openzeppelin-contracts/contracts/token/ERC20/IERC20.sol";
import "./SystemConfiguration.sol";

contract Challenge {
    SystemConfiguration public immutable SYSTEM_CONFIGURATION;

    constructor(SystemConfiguration configuration) {
        SYSTEM_CONFIGURATION = configuration;
    }

    function isSolved() external view returns (bool) {
        return IERC20(SYSTEM_CONFIGURATION.getStablecoin()).totalSupply() > 1_000_000_000_000 ether;
    }
}
