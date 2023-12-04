// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IWETH {
    function balanceOf(address account) external view returns (uint256);
    function totalSupply() external view returns (uint256);
    function allowance(address owner, address spender) external view returns (uint256);

    function transfer(address recipient, uint256 amount) external returns (bool);
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
    function approve(address spender, uint256 amount) external returns (bool);

    function deposit() external payable;
    function withdraw(uint256 amount) external;
}
