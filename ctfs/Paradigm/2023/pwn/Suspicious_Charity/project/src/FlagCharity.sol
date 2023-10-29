// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "../lib/openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";

contract FlagCharity {
    event Donated(address indexed user, address indexed token, uint256 amount);

    address public router;
    mapping(address => mapping(address => uint256)) public donation;

    modifier onlyRouter() {
        require(msg.sender == router);
        _;
    }

    constructor() {
        router = msg.sender;
    }

    function donate(address user, address token, uint256 amount) external onlyRouter {
        require(IERC20(token).transferFrom(msg.sender, address(this), amount), "FAIL_TRANSFER");

        donation[user][token] += amount;

        emit Donated(user, token, amount);
    }
}
