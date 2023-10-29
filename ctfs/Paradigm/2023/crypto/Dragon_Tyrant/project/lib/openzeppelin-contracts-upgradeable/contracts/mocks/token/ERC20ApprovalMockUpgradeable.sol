// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import { ERC20Upgradeable } from "../../token/ERC20/ERC20Upgradeable.sol";
import "../../proxy/utils/Initializable.sol";

abstract contract ERC20ApprovalMockUpgradeable is Initializable, ERC20Upgradeable {
    function __ERC20ApprovalMock_init() internal onlyInitializing {
    }

    function __ERC20ApprovalMock_init_unchained() internal onlyInitializing {
    }
    function _approve(address owner, address spender, uint256 amount, bool) internal virtual override {
        super._approve(owner, spender, amount, true);
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[50] private __gap;
}
