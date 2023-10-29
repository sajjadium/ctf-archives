// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import { IGovernorUpgradeable, GovernorUpgradeable } from "../../../governance/GovernorUpgradeable.sol";
import { GovernorCompatibilityBravoUpgradeable } from "../../../governance/compatibility/GovernorCompatibilityBravoUpgradeable.sol";
import { GovernorVotesUpgradeable } from "../../../governance/extensions/GovernorVotesUpgradeable.sol";
import { GovernorVotesQuorumFractionUpgradeable } from "../../../governance/extensions/GovernorVotesQuorumFractionUpgradeable.sol";
import { GovernorTimelockControlUpgradeable } from "../../../governance/extensions/GovernorTimelockControlUpgradeable.sol";
import { TimelockControllerUpgradeable } from "../../../governance/TimelockControllerUpgradeable.sol";
import { IVotesUpgradeable } from "../../../governance/utils/IVotesUpgradeable.sol";
import { IERC165Upgradeable } from "../../../interfaces/IERC165Upgradeable.sol";
import "../../../proxy/utils/Initializable.sol";

contract MyGovernorUpgradeable is
    Initializable, GovernorUpgradeable,
    GovernorCompatibilityBravoUpgradeable,
    GovernorVotesUpgradeable,
    GovernorVotesQuorumFractionUpgradeable,
    GovernorTimelockControlUpgradeable
{
    function __MyGovernor_init(
        IVotesUpgradeable _token,
        TimelockControllerUpgradeable _timelock
    ) internal onlyInitializing {
        __EIP712_init_unchained("MyGovernor", version());
        __Governor_init_unchained("MyGovernor");
        __GovernorVotes_init_unchained(_token);
        __GovernorVotesQuorumFraction_init_unchained(4);
        __GovernorTimelockControl_init_unchained(_timelock);
    }

    function __MyGovernor_init_unchained(
        IVotesUpgradeable,
        TimelockControllerUpgradeable
    ) internal onlyInitializing {}

    function votingDelay() public pure override returns (uint256) {
        return 7200; // 1 day
    }

    function votingPeriod() public pure override returns (uint256) {
        return 50400; // 1 week
    }

    function proposalThreshold() public pure override returns (uint256) {
        return 0;
    }

    // The functions below are overrides required by Solidity.

    function state(
        uint256 proposalId
    ) public view override(GovernorUpgradeable, IGovernorUpgradeable, GovernorTimelockControlUpgradeable) returns (ProposalState) {
        return super.state(proposalId);
    }

    function propose(
        address[] memory targets,
        uint256[] memory values,
        bytes[] memory calldatas,
        string memory description
    ) public override(GovernorUpgradeable, GovernorCompatibilityBravoUpgradeable, IGovernorUpgradeable) returns (uint256) {
        return super.propose(targets, values, calldatas, description);
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
    ) internal override(GovernorUpgradeable, GovernorTimelockControlUpgradeable) {
        super._execute(proposalId, targets, values, calldatas, descriptionHash);
    }

    function _cancel(
        address[] memory targets,
        uint256[] memory values,
        bytes[] memory calldatas,
        bytes32 descriptionHash
    ) internal override(GovernorUpgradeable, GovernorTimelockControlUpgradeable) returns (uint256) {
        return super._cancel(targets, values, calldatas, descriptionHash);
    }

    function _executor() internal view override(GovernorUpgradeable, GovernorTimelockControlUpgradeable) returns (address) {
        return super._executor();
    }

    function supportsInterface(
        bytes4 interfaceId
    ) public view override(GovernorUpgradeable, IERC165Upgradeable, GovernorTimelockControlUpgradeable) returns (bool) {
        return super.supportsInterface(interfaceId);
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[50] private __gap;
}
