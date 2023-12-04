// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./AirdropDistributor.sol";
import "./FrontrunBot.sol";
import "./IWETH.sol";

contract Challenge {
    IWETH public immutable weth;
    FrontrunBot public immutable bot;
    AirdropDistributor public immutable airdropDistributor;

    uint256 constant amount = 500 ether;
    uint256 constant claimableAmount = 100 ether;

    constructor(IWETH _weth, FrontrunBot _bot) payable {
        require(msg.value == amount + claimableAmount, "Challenge: wrong amount");

        airdropDistributor = new AirdropDistributor{value: claimableAmount}(_weth);
        weth = _weth;
        bot = _bot;

        weth.deposit{value: amount}();
        weth.transfer(address(_bot), amount);
    }

    function claim(string calldata password) external {
        uint256 value = airdropDistributor.claim(password);
        weth.transfer(msg.sender, value);
    }

    function isSolved() external view returns (bool) {
        return weth.balanceOf(address(this)) > amount + claimableAmount / 3;
    }
}
