// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

contract Challenge {
    function getScore() external view returns (uint256) {
        return address(this).balance / 1 ether;
    }
}
