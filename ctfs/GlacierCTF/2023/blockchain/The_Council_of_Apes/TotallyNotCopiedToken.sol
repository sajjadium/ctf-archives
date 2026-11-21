// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./libraries/ERC20.sol";

contract TotallyNotCopiedToken is ERC20 
{
    constructor(address owner, string memory name, string memory symbol) ERC20(name, symbol) 
    {
        _mint(owner, type(uint256).max);
    }
}