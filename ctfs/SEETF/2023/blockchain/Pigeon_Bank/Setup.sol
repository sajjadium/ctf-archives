// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;

import "./PETH.sol";
import "./PigeonBank.sol";

contract Setup {
    PETH public immutable peth;
    PigeonBank public immutable pigeonBank;

    // @dev - The SEE Team provided 2500 ETH to PigeonBank to provide liquidity so that the bank stays solvent.
    constructor() payable {
        require(msg.value == 2500 ether, "Setup: msg.value must be 2500 ether");
        pigeonBank = new PigeonBank();
        peth = pigeonBank.peth();

        // @dev - Deposit 2500 ETH to PigeonBank
        pigeonBank.deposit{value: msg.value}();

        assert(address(pigeonBank).balance == 0 ether);
        assert(peth.balanceOf(address(this)) == 2500 ether);
    }

    function isSolved() external view returns (bool) {
        return (peth.totalSupply() == 0) && (address(msg.sender).balance >= 2500 ether);
    }
}
