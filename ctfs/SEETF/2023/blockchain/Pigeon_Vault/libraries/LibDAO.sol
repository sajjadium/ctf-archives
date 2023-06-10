// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;

import {AppStorage, Proposal, LibAppStorage, Checkpoint} from "./LibAppStorage.sol";
import {IDiamondCut} from "../interfaces/IDiamondCut.sol";
import {LibDiamond} from "./LibDiamond.sol";

import {ECDSA} from "../libraries/ECDSA.sol";

library LibDAO {
    function submitProposal(address _target, bytes memory _callData, IDiamondCut.FacetCut memory _facetDetails)
        internal
        returns (uint256 proposalId)
    {
        AppStorage storage s = LibAppStorage.diamondStorage();

        proposalId = s.proposalCount;
        s.proposalCount++;

        Proposal storage newProposal = s.proposals[proposalId];

        newProposal.proposer = msg.sender;
        newProposal.target = _target;
        newProposal.callData = _callData;
        newProposal.startBlock = block.number;
        newProposal.endBlock = block.number + 6;
        newProposal.forVotes = 0;
        newProposal.againstVotes = 0;
        newProposal.canceled = false;
        newProposal.executed = false;
        newProposal.facetDetails = _facetDetails;
    }

    function getCurrentVotes(address _account) internal view returns (uint256) {
        AppStorage storage s = LibAppStorage.diamondStorage();

        uint32 nCheckpoints = s.numCheckpoints[_account];
        return nCheckpoints > 0 ? s.checkpoints[_account][nCheckpoints - 1].votes : 0;
    }

    function getPriorVotes(address _account, uint256 _blockNumber) internal view returns (uint256) {
        AppStorage storage s = LibAppStorage.diamondStorage();

        require(_blockNumber < block.number, "FTC: not yet determined");

        uint32 nCheckpoints = s.numCheckpoints[_account];
        if (nCheckpoints == 0) {
            return 0;
        }

        if (s.checkpoints[_account][nCheckpoints - 1].fromBlock <= _blockNumber) {
            return s.checkpoints[_account][nCheckpoints - 1].votes;
        }

        if (s.checkpoints[_account][0].fromBlock > _blockNumber) {
            return 0;
        }

        uint32 lower = 0;
        uint32 upper = nCheckpoints - 1;
        while (upper > lower) {
            uint32 center = upper - (upper - lower) / 2;
            Checkpoint memory cp = s.checkpoints[_account][center];
            if (cp.fromBlock == _blockNumber) {
                return cp.votes;
            } else if (cp.fromBlock < _blockNumber) {
                lower = center;
            } else {
                upper = center - 1;
            }
        }
        return s.checkpoints[_account][lower].votes;
    }
}
