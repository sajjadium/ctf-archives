// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import { ERC20Upgradeable } from "../../token/ERC20/ERC20Upgradeable.sol";
import "../../proxy/utils/Initializable.sol";

// contract that replicate USDT (0xdac17f958d2ee523a2206206994597c13d831ec7) approval beavior
abstract contract ERC20ForceApproveMockUpgradeable is Initializable, ERC20Upgradeable {
    function __ERC20ForceApproveMock_init() internal onlyInitializing {
    }

    function __ERC20ForceApproveMock_init_unchained() internal onlyInitializing {
    }
    function approve(address spender, uint256 amount) public virtual override returns (bool) {
        require(amount == 0 || allowance(msg.sender, spender) == 0, "USDT approval failure");
        return super.approve(spender, amount);
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[50] private __gap;
}
