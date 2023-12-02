// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.20;

interface IPancakeMigrator {
    function migrate(
        address token,
        uint256 amountTokenMin,
        uint256 amountETHMin,
        address to,
        uint256 deadline
    ) external;
}
