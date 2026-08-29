// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./PhantomVault.sol";

contract Setup {
    PhantomVault public vault;

    constructor(address _player) payable {
        vault = new PhantomVault{value: msg.value}(_player, _player);
    }

    function isSolved() external view returns (bool) {
        return address(vault).balance == 0;
    }
}
