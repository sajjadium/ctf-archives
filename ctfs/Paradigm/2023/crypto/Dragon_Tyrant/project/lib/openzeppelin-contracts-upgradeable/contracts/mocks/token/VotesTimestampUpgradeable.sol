// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import { ERC20VotesUpgradeable } from "../../token/ERC20/extensions/ERC20VotesUpgradeable.sol";
import { ERC721VotesUpgradeable } from "../../token/ERC721/extensions/ERC721VotesUpgradeable.sol";
import { SafeCastUpgradeable } from "../../utils/math/SafeCastUpgradeable.sol";
import "../../proxy/utils/Initializable.sol";

abstract contract ERC20VotesTimestampMockUpgradeable is Initializable, ERC20VotesUpgradeable {
    function __ERC20VotesTimestampMock_init() internal onlyInitializing {
    }

    function __ERC20VotesTimestampMock_init_unchained() internal onlyInitializing {
    }
    function clock() public view virtual override returns (uint48) {
        return SafeCastUpgradeable.toUint48(block.timestamp);
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

abstract contract ERC721VotesTimestampMockUpgradeable is Initializable, ERC721VotesUpgradeable {
    function __ERC721VotesTimestampMock_init() internal onlyInitializing {
    }

    function __ERC721VotesTimestampMock_init_unchained() internal onlyInitializing {
    }
    function clock() public view virtual override returns (uint48) {
        return SafeCastUpgradeable.toUint48(block.timestamp);
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
