// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

library PairName {
    function nextId(uint256 id) internal pure returns (uint256) {
        return id += 1;
    }

    function toString(uint256 value) internal pure returns (string memory) {
        return string(abi.encode(value));
    }
}
