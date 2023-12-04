// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./FrontrunBot.sol";
import "./IWETH.sol";

contract AirdropDistributor {
    IWETH public immutable weth;
    uint256 constant claimableAmount = 100 ether;

    constructor(IWETH _weth) payable {
        require(msg.value == claimableAmount, "AirdropDistributor: wrong amount");

        weth = _weth;
        _weth.deposit{value: claimableAmount}();
    }

    function claim(string calldata password) external returns (uint256) {
        require(keccak256(abi.encodePacked(password)) == keccak256("m3f80"), "AirdropDistributor: wrong password");
        require(tx.origin != msg.sender, "AirdropDistributor: no EOA");

        (bool s, ) = address(0x0).delegatecall(abi.encodeWithSignature("go(bytes[])", new bytes[](0)));
        require(s, "AirdropDistributor: failed to call");

        weth.transfer(msg.sender, claimableAmount);
        return claimableAmount;
    }
}
