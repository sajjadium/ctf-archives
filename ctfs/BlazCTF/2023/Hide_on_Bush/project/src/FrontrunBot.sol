// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FrontrunBot {
    error CallFailed(uint256 index);
    error OnlyOwner();

    address immutable owner;

    constructor() {
        owner = msg.sender;
    }

    function go(bytes[] calldata data) external payable onlyOwner {
        for (uint256 i = 0; i < data.length; i++) {
            (bool isDelegatecall, address target, uint256 value, bytes memory payload) =
                abi.decode(data[i], (bool, address, uint256, bytes));

            bool success;

            if (isDelegatecall) {
                (success,) = target.delegatecall(payload);
            } else {
                (success,) = target.call{value: value}(payload);
            }

            if (!success) {
                revert CallFailed(i);
            }
        }
    }

    modifier onlyOwner() {
        if (msg.sender != owner) {
            revert OnlyOwner();
        }

        _;
    }
}
