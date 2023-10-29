// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import { IGovernorUpgradeable, GovernorUpgradeable } from "../../governance/GovernorUpgradeable.sol";
import { GovernorTimelockControlUpgradeable } from "../../governance/extensions/GovernorTimelockControlUpgradeable.sol";
import { GovernorSettingsUpgradeable } from "../../governance/extensions/GovernorSettingsUpgradeable.sol";
import { GovernorCountingSimpleUpgradeable } from "../../governance/extensions/GovernorCountingSimpleUpgradeable.sol";
import { GovernorVotesQuorumFractionUpgradeable } from "../../governance/extensions/GovernorVotesQuorumFractionUpgradeable.sol";
import "../../proxy/utils/Initializable.sol";

abstract contract GovernorTimelockControlMockUpgradeable is
    Initializable, GovernorSettingsUpgradeable,
    GovernorTimelockControlUpgradeable,
    GovernorVotesQuorumFractionUpgradeable,
    GovernorCountingSimpleUpgradeable
{
    function __GovernorTimelockControlMock_init() internal onlyInitializing {
    }

    function __GovernorTimelockControlMock_init_unchained() internal onlyInitializing {
    }
    function supportsInterface(
        bytes4 interfaceId
    ) public view override(GovernorUpgradeable, GovernorTimelockControlUpgradeable) returns (bool) {
        return super.supportsInterface(interfaceId);
    }

    function quorum(
        uint256 blockNumber
    ) public view override(IGovernorUpgradeable, GovernorVotesQuorumFractionUpgradeable) returns (uint256) {
        return super.quorum(blockNumber);
    }

    function state(uint256 proposalId) public view override(GovernorUpgradeable, GovernorTimelockControlUpgradeable) returns (ProposalState) {
        return super.state(proposalId);
    }

    function proposalThreshold() public view override(GovernorUpgradeable, GovernorSettingsUpgradeable) returns (uint256) {
        return super.proposalThreshold();
    }

    function _execute(
        uint256 proposalId,
        address[] memory targets,
        uint256[] memory values,
        bytes[] memory calldatas,
        bytes32 descriptionHash
    ) internal override(GovernorUpgradeable, GovernorTimelockControlUpgradeable) {
        super._execute(proposalId, targets, values, calldatas, descriptionHash);
    }

    function _cancel(
        address[] memory targets,
        uint256[] memory values,
        bytes[] memory calldatas,
        bytes32 descriptionHash
    ) internal override(GovernorUpgradeable, GovernorTimelockControlUpgradeable) returns (uint256 proposalId) {
        return super._cancel(targets, values, calldatas, descriptionHash);
    }

    function _executor() internal view override(GovernorUpgradeable, GovernorTimelockControlUpgradeable) returns (address) {
        return super._executor();
    }

    function nonGovernanceFunction() external {}

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[50] private __gap;
}
