// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import { ERC20Upgradeable } from "../../token/ERC20/ERC20Upgradeable.sol";
import { MulticallUpgradeable } from "../../utils/MulticallUpgradeable.sol";
import "../../proxy/utils/Initializable.sol";

abstract contract ERC20MulticallMockUpgradeable is Initializable, ERC20Upgradeable, MulticallUpgradeable {    function __ERC20MulticallMock_init() internal onlyInitializing {
    }

    function __ERC20MulticallMock_init_unchained() internal onlyInitializing {
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[50] private __gap;
}
