// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import { IERC20Upgradeable, ERC20Upgradeable } from "../../../token/ERC20/ERC20Upgradeable.sol";
import { ERC20PermitUpgradeable } from "../../../token/ERC20/extensions/ERC20PermitUpgradeable.sol";
import { ERC20VotesUpgradeable } from "../../../token/ERC20/extensions/ERC20VotesUpgradeable.sol";
import { ERC20WrapperUpgradeable } from "../../../token/ERC20/extensions/ERC20WrapperUpgradeable.sol";
import { NoncesUpgradeable } from "../../../utils/NoncesUpgradeable.sol";
import "../../../proxy/utils/Initializable.sol";

contract MyTokenWrappedUpgradeable is Initializable, ERC20Upgradeable, ERC20PermitUpgradeable, ERC20VotesUpgradeable, ERC20WrapperUpgradeable {
    function __MyTokenWrapped_init(
        IERC20Upgradeable wrappedToken
    ) internal onlyInitializing {
        __ERC20_init_unchained("MyTokenWrapped", "MTK");
        __EIP712_init_unchained("MyTokenWrapped", "1");
        __ERC20Permit_init_unchained("MyTokenWrapped");
        __ERC20Wrapper_init_unchained(wrappedToken);
    }

    function __MyTokenWrapped_init_unchained(
        IERC20Upgradeable
    ) internal onlyInitializing {}

    // The functions below are overrides required by Solidity.

    function decimals() public view override(ERC20Upgradeable, ERC20WrapperUpgradeable) returns (uint8) {
        return super.decimals();
    }

    function _update(address from, address to, uint256 amount) internal override(ERC20Upgradeable, ERC20VotesUpgradeable) {
        super._update(from, to, amount);
    }

    function nonces(address owner) public view virtual override(ERC20PermitUpgradeable, NoncesUpgradeable) returns (uint256) {
        return super.nonces(owner);
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[50] private __gap;
}
