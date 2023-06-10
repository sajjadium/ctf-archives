// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.17;

import "./Pigeon.sol";

contract Setup {
    Pigeon public immutable pigeon;

    constructor() payable {
        pigeon = new Pigeon();

        // Junior Pigeons
        pigeon.assignPigeon("Numbuh", "6", address(0x006), 0);
        pigeon.assignPigeon{value: 5e18}("Numbuh", "5", address(0x005), 0);

        pigeon.assignPigeon("Numbuh", "4", address(0x004), 1);
        pigeon.assignPigeon{value: 10e18}("Numbuh", "3", address(0x003), 1);

        pigeon.assignPigeon("Numbuh", "2", address(0x002), 2);
        pigeon.assignPigeon{value: 15e18}("Numbuh", "1", address(0x001), 2);
    }

    receive() external payable {}

    function isSolved() external view returns (bool) {
        return address(msg.sender).balance >= 34 ether && address(pigeon).balance == 0 ether;
    }
}
