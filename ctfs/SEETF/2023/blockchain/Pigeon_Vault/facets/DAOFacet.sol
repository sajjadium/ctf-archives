// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;

import {AppStorage, Proposal} from "../libraries/LibAppStorage.sol";
import {LibDAO} from "../libraries/LibDAO.sol";
import {LibDiamond} from "../libraries/LibDiamond.sol";
import {IDiamondCut} from "../interfaces/IDiamondCut.sol";
import {IERC20} from "../interfaces/IERC20.sol";
import {ECDSA} from "../libraries/ECDSA.sol";

contract DAOFacet {
    AppStorage internal s;

    // Admin functions
    function setProposalThreshold(uint256 _proposalThreshold) external {
        LibDiamond.enforceIsContractOwner();
        s.proposalThreshold = _proposalThreshold;
    }

    function isUserGovernance(address _user) internal view returns (bool) {
        uint256 totalSupply = s.totalSupply;
        uint256 userBalance = LibDAO.getCurrentVotes(_user);
        uint256 threshold = (userBalance * 100) / totalSupply;
        return userBalance >= threshold;
    }

    function submitProposal(address _target, bytes memory _callData, IDiamondCut.FacetCut memory _facetDetails)
        external
        returns (uint256 proposalId)
    {
        require(
            msg.sender == LibDiamond.contractOwner() || isUserGovernance(msg.sender), "DAOFacet: Must be contract owner"
        );
        proposalId = LibDAO.submitProposal(_target, _callData, _facetDetails);
    }

    function executeProposal(uint256 _proposalId) external {
        Proposal storage proposal = s.proposals[_proposalId];
        require(!proposal.executed, "DAOFacet: Already executed.");
        require(block.number >= proposal.endBlock, "DAOFacet: Too early.");
        require(
            proposal.forVotes > proposal.againstVotes && proposal.forVotes > (s.totalSupply / 10),
            "DAOFacet: Proposal failed."
        );
        proposal.executed = true;

        IDiamondCut.FacetCut[] memory cut = new IDiamondCut.FacetCut[](1);

        cut[0] = IDiamondCut.FacetCut({
            facetAddress: proposal.target,
            action: proposal.facetDetails.action,
            functionSelectors: proposal.facetDetails.functionSelectors
        });

        LibDiamond.diamondCut(cut, proposal.target, proposal.callData);
    }

    function castVoteBySig(uint256 _proposalId, bool _support, bytes memory _sig) external {
        address signer = ECDSA.recover(keccak256("\x19Ethereum Signed Message:\n32"), _sig);
        require(signer != address(0), "DAOFacet: Invalid signature.");
        _vote(_sig, _proposalId, _support);
    }

    function _vote(bytes memory _sig, uint256 _proposalId, bool _support) internal {
        Proposal storage proposal = s.proposals[_proposalId];
        require(LibDAO.getPriorVotes(msg.sender, proposal.startBlock) >= s.voteThreshold, "DAOFacet: Not enough.");
        require(block.number <= s.proposals[_proposalId].endBlock, "DAOFacet: Too late.");
        bool hasVoted = proposal.receipts[_sig];
        require(!hasVoted, "DAOFacet: Already voted.");
        uint256 votes = LibDAO.getPriorVotes(msg.sender, proposal.startBlock);

        if (_support) {
            proposal.forVotes += votes;
        } else {
            proposal.againstVotes += votes;
        }

        proposal.receipts[_sig] = true;
    }
}
