// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/Address.sol";

import "./PETH.sol";

// Deposit Ether to PigeonBank to get PETH
// @TODO: Implement interest rate feature so that users can get interest by depositing Ether
contract PigeonBank is ReentrancyGuard {
    using Address for address payable;
    using Address for address;

    PETH public immutable peth; // @dev - Created by the SEE team. Pigeon Bank is created to allow citizens to deposit Ether and get SEETH and earn interest to survive the economic crisis.
    address private _owner;

    constructor() {
        peth = new PETH();
        _owner = msg.sender;
    }

    function deposit() public payable nonReentrant {
        peth.deposit{value: msg.value}(msg.sender);
    }

    function withdraw(uint256 wad) public nonReentrant {
        peth.withdraw(msg.sender, wad);
    }

    function withdrawAll() public nonReentrant {
        peth.withdrawAll(msg.sender);
    }

    function flashLoan(address receiver, bytes calldata data, uint256 wad) public nonReentrant {
        peth.flashLoan(receiver, wad, data);
    }

    receive() external payable {}
}
