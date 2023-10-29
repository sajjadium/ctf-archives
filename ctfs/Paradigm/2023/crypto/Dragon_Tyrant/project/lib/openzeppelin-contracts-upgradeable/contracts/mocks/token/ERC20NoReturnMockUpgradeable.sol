// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import { ERC20Upgradeable } from "../../token/ERC20/ERC20Upgradeable.sol";
import "../../proxy/utils/Initializable.sol";

abstract contract ERC20NoReturnMockUpgradeable is Initializable, ERC20Upgradeable {
    function __ERC20NoReturnMock_init() internal onlyInitializing {
    }

    function __ERC20NoReturnMock_init_unchained() internal onlyInitializing {
    }
    function transfer(address to, uint256 amount) public override returns (bool) {
        super.transfer(to, amount);
        assembly {
            return(0, 0)
        }
    }

    function transferFrom(address from, address to, uint256 amount) public override returns (bool) {
        super.transferFrom(from, to, amount);
        assembly {
            return(0, 0)
        }
    }

    function approve(address spender, uint256 amount) public override returns (bool) {
        super.approve(spender, amount);
        assembly {
            return(0, 0)
        }
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[50] private __gap;
}
