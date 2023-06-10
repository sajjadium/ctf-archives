// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;

import {AppStorage, Proposal} from "../libraries/LibAppStorage.sol";
import {IDiamondCut} from "../interfaces/IDiamondCut.sol";
import {IERC20} from "../interfaces/IERC20.sol";

interface IDAOFacet {
    function setProposalThreshold(uint256 _proposalThreshold) external;
    function isUserGovernance(address _user) external view returns (bool);
    function submitProposal(address _target, bytes memory _callData, IDiamondCut.FacetCut memory _facetDetails)
        external
        returns (uint256 proposalId);
    function executeProposal(uint256 _proposalId) external;
    function castVoteBySig(uint256 _proposalId, bool _support, bytes memory _sig) external;
}
