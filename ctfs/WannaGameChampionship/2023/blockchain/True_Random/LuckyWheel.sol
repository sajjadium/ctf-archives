// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;

contract LuckyWheel {
    uint256 public closed;

    constructor() payable {}

    modifier onlyEOA() {
        require(!isContract(msg.sender), "LuckyWheel: ONLY_EOA");
        _;
    }

    function isContract(address addr) internal view returns (bool) {
        uint256 size;
        assembly {
            size := extcodesize(addr)
        }
        return size > 0;
    }

    function wannaLuck(uint256 seed) external payable onlyEOA {
        require(msg.value == 0.1 ether, "LuckyWheel: INVALID_AMOUNT");
        uint256 random = uint256(keccak256(abi.encodePacked(seed, block.timestamp, msg.sender)));
        if (random % 100 == 0) {
            closed = 1;
        }
    }
}
