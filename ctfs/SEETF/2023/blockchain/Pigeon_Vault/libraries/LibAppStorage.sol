// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;

import {Counters} from "@openzeppelin/contracts/utils/Counters.sol";

import {IERC20} from "../interfaces/IERC20.sol";
import {IDiamondCut} from "../interfaces/IDiamondCut.sol";

struct Proposal {
    address proposer;
    address target;
    bytes callData;
    uint256 startBlock;
    uint256 endBlock;
    uint256 forVotes;
    uint256 againstVotes;
    bool canceled;
    bool executed;
    IDiamondCut.FacetCut facetDetails;
    mapping(bytes => bool) receipts;
}

struct Checkpoint {
    uint32 fromBlock;
    uint256 votes;
}

struct AppStorage {
    uint256 totalSupply;
    mapping(address => mapping(address => uint256)) allowances;
    mapping(address => uint256) balances;
    mapping(address => address) delegates;
    mapping(address => mapping(uint32 => Checkpoint)) checkpoints;
    mapping(address => uint32) numCheckpoints;
    uint256 proposalThreshold;
    uint256 voteThreshold;
    uint256 proposalCount;
    IERC20 governanceToken;
    mapping(uint256 => Proposal) proposals;
    address pigeonVaultFacet;
}

library LibAppStorage {
    function diamondStorage() internal pure returns (AppStorage storage s) {
        assembly {
            s.slot := 0
        }
    }
}
