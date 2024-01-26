// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {IL1ERC20Bridge} from "./IL1ERC20Bridge.sol";
import {IL2ERC20Bridge} from "../L2/IL2ERC20Bridge.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

import {CrossDomainEnabled} from "../libraries/bridge/CrossDomainEnabled.sol";
import {Lib_PredeployAddresses} from "../libraries/constants/Lib_PredeployAddresses.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

/**
 * @title L1ERC20Bridge
 * @dev The L1 ERC20 Bridge is a contract which stores deposited L1 funds and standard
 * tokens that are in use on L2. It synchronizes a corresponding L2 Bridge, informing it of deposits
 * and listening to it for newly finalized withdrawals.
 *
 */
contract L1ERC20Bridge is IL1ERC20Bridge, CrossDomainEnabled {
    using SafeERC20 for IERC20;

    address public l2TokenBridge;
    address public weth;
    // Maps L1 token to L2 token to balance of the L1 token deposited
    mapping(address => mapping(address => uint256)) public deposits;

    constructor(address _l1messenger, address _l2TokenBridge, address _weth) CrossDomainEnabled(_l1messenger) {
        l2TokenBridge = _l2TokenBridge;
        weth = _weth;
    }

    /**
     * @inheritdoc IL1ERC20Bridge
     */
    function depositERC20(address _l1Token, address _l2Token, uint256 _amount) external virtual {
        _initiateERC20Deposit(_l1Token, _l2Token, msg.sender, msg.sender, _amount);
    }

    /**
     * @inheritdoc IL1ERC20Bridge
     */
    function depositERC20To(address _l1Token, address _l2Token, address _to, uint256 _amount) external virtual {
        _initiateERC20Deposit(_l1Token, _l2Token, msg.sender, _to, _amount);
    }

    function _initiateERC20Deposit(address _l1Token, address _l2Token, address _from, address _to, uint256 _amount)
        internal
    {
        IERC20(_l1Token).safeTransferFrom(_from, address(this), _amount);

        bytes memory message;
        if (_l1Token == weth) {
            message = abi.encodeWithSelector(
                IL2ERC20Bridge.finalizeDeposit.selector, address(0), Lib_PredeployAddresses.L2_WETH, _from, _to, _amount
            );
        } else {
            message =
                abi.encodeWithSelector(IL2ERC20Bridge.finalizeDeposit.selector, _l1Token, _l2Token, _from, _to, _amount);
        }

        sendCrossDomainMessage(l2TokenBridge, message);
        deposits[_l1Token][_l2Token] = deposits[_l1Token][_l2Token] + _amount;

        emit ERC20DepositInitiated(_l1Token, _l2Token, _from, _to, _amount);
    }

    /**
     * @inheritdoc IL1ERC20Bridge
     */
    function finalizeERC20Withdrawal(address _l1Token, address _l2Token, address _from, address _to, uint256 _amount)
        public
        onlyFromCrossDomainAccount(l2TokenBridge)
    {
        deposits[_l1Token][_l2Token] = deposits[_l1Token][_l2Token] - _amount;
        IERC20(_l1Token).safeTransfer(_to, _amount);
        emit ERC20WithdrawalFinalized(_l1Token, _l2Token, _from, _to, _amount);
    }

    /**
     * @inheritdoc IL1ERC20Bridge
     */
    function finalizeWethWithdrawal(address _from, address _to, uint256 _amount)
        external
        onlyFromCrossDomainAccount(l2TokenBridge)
    {
        finalizeERC20Withdrawal(weth, Lib_PredeployAddresses.L2_WETH, _from, _to, _amount);
    }
}
