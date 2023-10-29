// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import { IERC20Upgradeable, ERC20Upgradeable } from "../../token/ERC20/ERC20Upgradeable.sol";
import { ERC4626Upgradeable } from "../../token/ERC20/extensions/ERC4626Upgradeable.sol";
import "../../proxy/utils/Initializable.sol";

contract ERC4626MockUpgradeable is Initializable, ERC4626Upgradeable {
    function __ERC4626Mock_init(address underlying) internal onlyInitializing {
        __ERC20_init_unchained("ERC4626Mock", "E4626M");
        __ERC4626_init_unchained(IERC20Upgradeable(underlying));
    }

    function __ERC4626Mock_init_unchained(address) internal onlyInitializing {}

    function mint(address account, uint256 amount) external {
        _mint(account, amount);
    }

    function burn(address account, uint256 amount) external {
        _burn(account, amount);
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[50] private __gap;
}
