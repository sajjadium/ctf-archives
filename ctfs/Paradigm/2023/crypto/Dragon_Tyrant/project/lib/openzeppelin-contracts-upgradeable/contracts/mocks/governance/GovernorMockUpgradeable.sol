// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import { GovernorUpgradeable } from "../../governance/GovernorUpgradeable.sol";
import { GovernorSettingsUpgradeable } from "../../governance/extensions/GovernorSettingsUpgradeable.sol";
import { GovernorCountingSimpleUpgradeable } from "../../governance/extensions/GovernorCountingSimpleUpgradeable.sol";
import { GovernorVotesQuorumFractionUpgradeable } from "../../governance/extensions/GovernorVotesQuorumFractionUpgradeable.sol";
import "../../proxy/utils/Initializable.sol";

abstract contract GovernorMockUpgradeable is Initializable, GovernorSettingsUpgradeable, GovernorVotesQuorumFractionUpgradeable, GovernorCountingSimpleUpgradeable {
    function __GovernorMock_init() internal onlyInitializing {
    }

    function __GovernorMock_init_unchained() internal onlyInitializing {
    }
    function proposalThreshold() public view override(GovernorUpgradeable, GovernorSettingsUpgradeable) returns (uint256) {
        return super.proposalThreshold();
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[50] private __gap;
}
