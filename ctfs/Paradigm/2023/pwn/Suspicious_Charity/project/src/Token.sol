// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "../lib/openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";

contract Token is ERC20 {
    address public tokenFactory;

    modifier onlyFactory() {
        require(msg.sender == tokenFactory);
        _;
    }

    constructor(string memory name_, string memory symbol_) ERC20(name_, symbol_) {
        tokenFactory = msg.sender;
    }

    function mint(address account, uint256 amount) external onlyFactory {
        _mint(account, amount);
    }
}
