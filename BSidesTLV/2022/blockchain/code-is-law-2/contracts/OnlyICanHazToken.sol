//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.0;

contract OnlyICanHazToken {
    function bye() public {
        selfdestruct(payable(msg.sender));
    }
}
