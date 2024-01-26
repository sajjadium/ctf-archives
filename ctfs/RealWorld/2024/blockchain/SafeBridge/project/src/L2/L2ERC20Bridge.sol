// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {IL1ERC20Bridge} from "../L1/IL1ERC20Bridge.sol";
import {IL2ERC20Bridge} from "./IL2ERC20Bridge.sol";

import {ERC165Checker} from "@openzeppelin/contracts/utils/introspection/ERC165Checker.sol";
import {CrossDomainEnabled} from "../libraries/bridge/CrossDomainEnabled.sol";
import {Lib_PredeployAddresses} from "../libraries/constants/Lib_PredeployAddresses.sol";

import {IL2StandardERC20} from "./standards/IL2StandardERC20.sol";

/**
 * @title L2ERC20Bridge
 * @dev The L2 Standard bridge is a contract which works together with the L1 Standard bridge to
 * enable ETH and ERC20 transitions between L1 and L2.
 * This contract acts as a minter for new tokens when it hears about deposits into the L1 Standard
 * bridge.
 * This contract also acts as a burner of the tokens intended for withdrawal, informing the L1
 * bridge to release L1 funds.
 */
contract L2ERC20Bridge is IL2ERC20Bridge, CrossDomainEnabled {
    address public l1TokenBridge;

    constructor(address _l2messenger, address _l1TokenBridge) CrossDomainEnabled(_l2messenger) {
        l1TokenBridge = _l1TokenBridge;
    }

    /**
     * @inheritdoc IL2ERC20Bridge
     */
    function withdraw(address _l2Token, uint256 _amount) external virtual {
        _initiateWithdrawal(_l2Token, msg.sender, msg.sender, _amount);
    }

    /**
     * @inheritdoc IL2ERC20Bridge
     */
    function withdrawTo(address _l2Token, address _to, uint256 _amount) external virtual {
        _initiateWithdrawal(_l2Token, msg.sender, _to, _amount);
    }

    function _initiateWithdrawal(address _l2Token, address _from, address _to, uint256 _amount) internal {
        IL2StandardERC20(_l2Token).burn(msg.sender, _amount);

        address l1Token = IL2StandardERC20(_l2Token).l1Token();
        bytes memory message;
        if (_l2Token == Lib_PredeployAddresses.L2_WETH) {
            message = abi.encodeWithSelector(IL1ERC20Bridge.finalizeWethWithdrawal.selector, _from, _to, _amount);
        } else {
            message = abi.encodeWithSelector(
                IL1ERC20Bridge.finalizeERC20Withdrawal.selector, l1Token, _l2Token, _from, _to, _amount
            );
        }

        sendCrossDomainMessage(l1TokenBridge, message);

        emit WithdrawalInitiated(l1Token, _l2Token, msg.sender, _to, _amount);
    }

    /**
     * @inheritdoc IL2ERC20Bridge
     */
    function finalizeDeposit(address _l1Token, address _l2Token, address _from, address _to, uint256 _amount)
        external
        virtual
        onlyFromCrossDomainAccount(l1TokenBridge)
    {
        // Check the target token is compliant and
        // verify the deposited token on L1 matches the L2 deposited token representation here
        if (ERC165Checker.supportsInterface(_l2Token, 0x1d1d8b63) && _l1Token == IL2StandardERC20(_l2Token).l1Token()) {
            IL2StandardERC20(_l2Token).mint(_to, _amount);
            emit DepositFinalized(_l1Token, _l2Token, _from, _to, _amount);
        } else {
            emit DepositFailed(_l1Token, _l2Token, _from, _to, _amount);
        }
    }
}
