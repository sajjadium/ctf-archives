Welcome to the LendingPool challenge! In this challenge, you'll be diving into a pool that offers flash loans of CTF tokens for free. The pool currently holds a balance of 1 million CTF tokens, while you start with nothing. However, there's no need to worry – you just might have what it takes to acquire them all from the pool.
LendingPool

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;


import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/security/ReentrancyGuard.sol";


contract LendingPool is ReentrancyGuard {
IERC20 public ctfToken;


constructor(address tokenAddress) {
    ctfToken = IERC20(tokenAddress);
}


function flashLoan(uint256 borrowAmount, address borrower, address target,          bytes calldata data)
external
nonReentrant
{
    uint256 balanceBefore = ctfToken.balanceOf(address(this));
    require(balanceBefore >= borrowAmount, "Not enough tokens in pool");


    ctfToken.transfer(borrower, borrowAmount);
    (bool success,) = target.call(data);
    require(success, "External call failed");


    uint256 balanceAfter = ctfToken.balanceOf(address(this));
    require(balanceAfter >= balanceBefore, "Flash loan hasn't been paid back");
}


function isSolved() public view returns (bool) {
    return ctfToken.balanceOf(address(this)) == 0;
}
}

CTF Token

https://mumbai.polygonscan.com/address/0xfa8994aa87c97e291dc8f08d88d76a1c623474d7

Note: To participate in this challenge, please ensure you possess Mumbai Testnet Matic tokens. https://mumbaifaucet.com/

The website is available at: https://lending.uctf.ir/
