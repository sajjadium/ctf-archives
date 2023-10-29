// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import { IERC20Upgradeable } from "../../token/ERC20/IERC20Upgradeable.sol";
import { ERC4626Upgradeable } from "../../token/ERC20/extensions/ERC4626Upgradeable.sol";
import { SafeERC20Upgradeable } from "../../token/ERC20/utils/SafeERC20Upgradeable.sol";
import { MathUpgradeable } from "../../utils/math/MathUpgradeable.sol";
import "../../proxy/utils/Initializable.sol";

abstract contract ERC4626FeesUpgradeable is Initializable, ERC4626Upgradeable {
    function __ERC4626Fees_init() internal onlyInitializing {
    }

    function __ERC4626Fees_init_unchained() internal onlyInitializing {
    }
    using MathUpgradeable for uint256;

    /** @dev See {IERC4626-previewDeposit}. */
    function previewDeposit(uint256 assets) public view virtual override returns (uint256) {
        uint256 fee = _feeOnTotal(assets, _entryFeeBasePoint());
        return super.previewDeposit(assets - fee);
    }

    /** @dev See {IERC4626-previewMint}. */
    function previewMint(uint256 shares) public view virtual override returns (uint256) {
        uint256 assets = super.previewMint(shares);
        return assets + _feeOnRaw(assets, _entryFeeBasePoint());
    }

    /** @dev See {IERC4626-previewWithdraw}. */
    function previewWithdraw(uint256 assets) public view virtual override returns (uint256) {
        uint256 fee = _feeOnRaw(assets, _exitFeeBasePoint());
        return super.previewWithdraw(assets + fee);
    }

    /** @dev See {IERC4626-previewRedeem}. */
    function previewRedeem(uint256 shares) public view virtual override returns (uint256) {
        uint256 assets = super.previewRedeem(shares);
        return assets - _feeOnTotal(assets, _exitFeeBasePoint());
    }

    /** @dev See {IERC4626-_deposit}. */
    function _deposit(address caller, address receiver, uint256 assets, uint256 shares) internal virtual override {
        uint256 fee = _feeOnTotal(assets, _entryFeeBasePoint());
        address recipient = _entryFeeRecipient();

        super._deposit(caller, receiver, assets, shares);

        if (fee > 0 && recipient != address(this)) {
            SafeERC20Upgradeable.safeTransfer(IERC20Upgradeable(asset()), recipient, fee);
        }
    }

    /** @dev See {IERC4626-_deposit}. */
    function _withdraw(
        address caller,
        address receiver,
        address owner,
        uint256 assets,
        uint256 shares
    ) internal virtual override {
        uint256 fee = _feeOnRaw(assets, _exitFeeBasePoint());
        address recipient = _exitFeeRecipient();

        super._withdraw(caller, receiver, owner, assets, shares);

        if (fee > 0 && recipient != address(this)) {
            SafeERC20Upgradeable.safeTransfer(IERC20Upgradeable(asset()), recipient, fee);
        }
    }

    function _entryFeeBasePoint() internal view virtual returns (uint256) {
        return 0;
    }

    function _entryFeeRecipient() internal view virtual returns (address) {
        return address(0);
    }

    function _exitFeeBasePoint() internal view virtual returns (uint256) {
        return 0;
    }

    function _exitFeeRecipient() internal view virtual returns (address) {
        return address(0);
    }

    function _feeOnRaw(uint256 assets, uint256 feeBasePoint) private pure returns (uint256) {
        return assets.mulDiv(feeBasePoint, 1e5, MathUpgradeable.Rounding.Ceil);
    }

    function _feeOnTotal(uint256 assets, uint256 feeBasePoint) private pure returns (uint256) {
        return assets.mulDiv(feeBasePoint, feeBasePoint + 1e5, MathUpgradeable.Rounding.Ceil);
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[50] private __gap;
}
