// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import { VotesUpgradeable } from "../governance/utils/VotesUpgradeable.sol";
import "../proxy/utils/Initializable.sol";

abstract contract VotesMockUpgradeable is Initializable, VotesUpgradeable {
    function __VotesMock_init() internal onlyInitializing {
    }

    function __VotesMock_init_unchained() internal onlyInitializing {
    }
    mapping(address => uint256) private _votingUnits;

    function getTotalSupply() public view returns (uint256) {
        return _getTotalSupply();
    }

    function delegate(address account, address newDelegation) public {
        return _delegate(account, newDelegation);
    }

    function _getVotingUnits(address account) internal view override returns (uint256) {
        return _votingUnits[account];
    }

    function _mint(address account, uint256 votes) internal {
        _votingUnits[account] += votes;
        _transferVotingUnits(address(0), account, votes);
    }

    function _burn(address account, uint256 votes) internal {
        _votingUnits[account] += votes;
        _transferVotingUnits(account, address(0), votes);
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[49] private __gap;
}

abstract contract VotesTimestampMockUpgradeable is Initializable, VotesMockUpgradeable {
    function __VotesTimestampMock_init() internal onlyInitializing {
    }

    function __VotesTimestampMock_init_unchained() internal onlyInitializing {
    }
    function clock() public view override returns (uint48) {
        return uint48(block.timestamp);
    }

    // solhint-disable-next-line func-name-mixedcase
    function CLOCK_MODE() public view virtual override returns (string memory) {
        return "mode=timestamp";
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[50] private __gap;
}
