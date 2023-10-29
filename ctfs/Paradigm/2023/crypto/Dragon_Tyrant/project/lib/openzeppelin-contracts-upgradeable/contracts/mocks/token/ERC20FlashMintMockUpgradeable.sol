// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import { ERC20FlashMintUpgradeable } from "../../token/ERC20/extensions/ERC20FlashMintUpgradeable.sol";
import "../../proxy/utils/Initializable.sol";

abstract contract ERC20FlashMintMockUpgradeable is Initializable, ERC20FlashMintUpgradeable {
    function __ERC20FlashMintMock_init() internal onlyInitializing {
    }

    function __ERC20FlashMintMock_init_unchained() internal onlyInitializing {
    }
    uint256 _flashFeeAmount;
    address _flashFeeReceiverAddress;

    function setFlashFee(uint256 amount) public {
        _flashFeeAmount = amount;
    }

    function _flashFee(address, uint256) internal view override returns (uint256) {
        return _flashFeeAmount;
    }

    function setFlashFeeReceiver(address receiver) public {
        _flashFeeReceiverAddress = receiver;
    }

    function _flashFeeReceiver() internal view override returns (address) {
        return _flashFeeReceiverAddress;
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[48] private __gap;
}
