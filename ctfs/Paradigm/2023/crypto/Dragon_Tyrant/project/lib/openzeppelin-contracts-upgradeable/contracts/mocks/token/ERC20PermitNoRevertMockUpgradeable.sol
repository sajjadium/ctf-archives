// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import { ERC20PermitUpgradeable } from "../../token/ERC20/extensions/ERC20PermitUpgradeable.sol";
import "../../proxy/utils/Initializable.sol";

abstract contract ERC20PermitNoRevertMockUpgradeable is Initializable, ERC20PermitUpgradeable {
    function __ERC20PermitNoRevertMock_init() internal onlyInitializing {
    }

    function __ERC20PermitNoRevertMock_init_unchained() internal onlyInitializing {
    }
    function permitThatMayRevert(
        address owner,
        address spender,
        uint256 value,
        uint256 deadline,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) public virtual {
        super.permit(owner, spender, value, deadline, v, r, s);
    }

    function permit(
        address owner,
        address spender,
        uint256 value,
        uint256 deadline,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) public virtual override {
        try this.permitThatMayRevert(owner, spender, value, deadline, v, r, s) {
            // do nothing
        } catch {
            // do nothing
        }
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[50] private __gap;
}
