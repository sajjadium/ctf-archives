// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v4.9.0) (token/ERC20/extensions/ERC20Wrapper.sol)

pragma solidity ^0.8.19;

import { IERC20Upgradeable, IERC20MetadataUpgradeable, ERC20Upgradeable } from "../ERC20Upgradeable.sol";
import { SafeERC20Upgradeable } from "../utils/SafeERC20Upgradeable.sol";
import "../../../proxy/utils/Initializable.sol";

/**
 * @dev Extension of the ERC20 token contract to support token wrapping.
 *
 * Users can deposit and withdraw "underlying tokens" and receive a matching number of "wrapped tokens". This is useful
 * in conjunction with other modules. For example, combining this wrapping mechanism with {ERC20Votes} will allow the
 * wrapping of an existing "basic" ERC20 into a governance token.
 */
abstract contract ERC20WrapperUpgradeable is Initializable, ERC20Upgradeable {
    IERC20Upgradeable private _underlying;

    /**
     * @dev The underlying token couldn't be wrapped.
     */
    error ERC20InvalidUnderlying(address token);

    function __ERC20Wrapper_init(IERC20Upgradeable underlyingToken) internal onlyInitializing {
        __ERC20Wrapper_init_unchained(underlyingToken);
    }

    function __ERC20Wrapper_init_unchained(IERC20Upgradeable underlyingToken) internal onlyInitializing {
        if (underlyingToken == this) {
            revert ERC20InvalidUnderlying(address(this));
        }
        _underlying = underlyingToken;
    }

    /**
     * @dev See {ERC20-decimals}.
     */
    function decimals() public view virtual override returns (uint8) {
        try IERC20MetadataUpgradeable(address(_underlying)).decimals() returns (uint8 value) {
            return value;
        } catch {
            return super.decimals();
        }
    }

    /**
     * @dev Returns the address of the underlying ERC-20 token that is being wrapped.
     */
    function underlying() public view returns (IERC20Upgradeable) {
        return _underlying;
    }

    /**
     * @dev Allow a user to deposit underlying tokens and mint the corresponding number of wrapped tokens.
     */
    function depositFor(address account, uint256 value) public virtual returns (bool) {
        address sender = _msgSender();
        if (sender == address(this)) {
            revert ERC20InvalidSender(address(this));
        }
        if (account == address(this)) {
            revert ERC20InvalidReceiver(account);
        }
        SafeERC20Upgradeable.safeTransferFrom(_underlying, sender, address(this), value);
        _mint(account, value);
        return true;
    }

    /**
     * @dev Allow a user to burn a number of wrapped tokens and withdraw the corresponding number of underlying tokens.
     */
    function withdrawTo(address account, uint256 value) public virtual returns (bool) {
        if (account == address(this)) {
            revert ERC20InvalidReceiver(account);
        }
        _burn(_msgSender(), value);
        SafeERC20Upgradeable.safeTransfer(_underlying, account, value);
        return true;
    }

    /**
     * @dev Mint wrapped token to cover any underlyingTokens that would have been transferred by mistake. Internal
     * function that can be exposed with access control if desired.
     */
    function _recover(address account) internal virtual returns (uint256) {
        uint256 value = _underlying.balanceOf(address(this)) - totalSupply();
        _mint(account, value);
        return value;
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[49] private __gap;
}
