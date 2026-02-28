// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Governance {

    uint256 public proposalCount;   

    function setProposal(uint256 x) public {
        proposalCount = x;
    }
}