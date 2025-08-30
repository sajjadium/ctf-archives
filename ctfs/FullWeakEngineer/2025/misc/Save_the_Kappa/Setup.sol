// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import "./VulnerableBank.sol";

contract Setup {
    VulnerableBank public immutable bank;

    constructor() payable {
        VulnerableBank _b = new VulnerableBank();
        if (msg.value > 0) {
            (bool ok, ) = address(_b).call{value: msg.value}("");
            require(ok, "seed failed");
        }
        bank = _b;
    }

    function getBank() external view returns (address) {
        return address(bank);
    }

    function isSolved() external view returns (bool) {
        return address(bank).balance == 0;
    }
}
