// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import { IGovernorUpgradeable, GovernorUpgradeable } from "../../governance/GovernorUpgradeable.sol";
import { GovernorCompatibilityBravoUpgradeable } from "../../governance/compatibility/GovernorCompatibilityBravoUpgradeable.sol";
import { IGovernorTimelockUpgradeable, GovernorTimelockCompoundUpgradeable } from "../../governance/extensions/GovernorTimelockCompoundUpgradeable.sol";
import { GovernorSettingsUpgradeable } from "../../governance/extensions/GovernorSettingsUpgradeable.sol";
import { GovernorVotesUpgradeable } from "../../governance/extensions/GovernorVotesUpgradeable.sol";
import { IERC165Upgradeable } from "../../interfaces/IERC165Upgradeable.sol";
import "../../proxy/utils/Initializable.sol";

abstract contract GovernorCompatibilityBravoMockUpgradeable is
    Initializable, GovernorCompatibilityBravoUpgradeable,
    GovernorSettingsUpgradeable,
    GovernorTimelockCompoundUpgradeable,
    GovernorVotesUpgradeable
{
    function __GovernorCompatibilityBravoMock_init() internal onlyInitializing {
    }

    function __GovernorCompatibilityBravoMock_init_unchained() internal onlyInitializing {
    }
    function quorum(uint256) public pure override returns (uint256) {
        return 0;
    }

    function supportsInterface(
        bytes4 interfaceId
    ) public view override(IERC165Upgradeable, GovernorUpgradeable, GovernorTimelockCompoundUpgradeable) returns (bool) {
        return super.supportsInterface(interfaceId);
    }

    function state(
        uint256 proposalId
    ) public view override(IGovernorUpgradeable, GovernorUpgradeable, GovernorTimelockCompoundUpgradeable) returns (ProposalState) {
        return super.state(proposalId);
    }

    function proposalEta(
        uint256 proposalId
    ) public view override(IGovernorTimelockUpgradeable, GovernorTimelockCompoundUpgradeable) returns (uint256) {
        return super.proposalEta(proposalId);
    }

    function proposalThreshold() public view override(GovernorUpgradeable, GovernorSettingsUpgradeable) returns (uint256) {
        return super.proposalThreshold();
    }

    function propose(
        address[] memory targets,
        uint256[] memory values,
        bytes[] memory calldatas,
        string memory description
    ) public override(IGovernorUpgradeable, GovernorUpgradeable, GovernorCompatibilityBravoUpgradeable) returns (uint256) {
        return super.propose(targets, values, calldatas, description);
    }

    function queue(
        address[] memory targets,
        uint256[] memory values,
        bytes[] memory calldatas,
        bytes32 salt
    ) public override(IGovernorTimelockUpgradeable, GovernorTimelockCompoundUpgradeable) returns (uint256) {
        return super.queue(targets, values, calldatas, salt);
    }

    function execute(
        address[] memory targets,
        uint256[] memory values,
        bytes[] memory calldatas,
        bytes32 salt
    ) public payable override(IGovernorUpgradeable, GovernorUpgradeable) returns (uint256) {
        return super.execute(targets, values, calldatas, salt);
    }

    function cancel(
        address[] memory targets,
        uint256[] memory values,
        bytes[] memory calldatas,
        bytes32 descriptionHash
    ) public override(GovernorUpgradeable, GovernorCompatibilityBravoUpgradeable, IGovernorUpgradeable) returns (uint256) {
        return super.cancel(targets, values, calldatas, descriptionHash);
    }

    function _execute(
        uint256 proposalId,
        address[] memory targets,
        uint256[] memory values,
        bytes[] memory calldatas,
        bytes32 descriptionHash
    ) internal override(GovernorUpgradeable, GovernorTimelockCompoundUpgradeable) {
        super._execute(proposalId, targets, values, calldatas, descriptionHash);
    }

    function _cancel(
        address[] memory targets,
        uint256[] memory values,
        bytes[] memory calldatas,
        bytes32 salt
    ) internal override(GovernorUpgradeable, GovernorTimelockCompoundUpgradeable) returns (uint256 proposalId) {
        return super._cancel(targets, values, calldatas, salt);
    }

    function _executor() internal view override(GovernorUpgradeable, GovernorTimelockCompoundUpgradeable) returns (address) {
        return super._executor();
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[50] private __gap;
}
