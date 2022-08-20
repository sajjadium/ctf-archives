// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.16;

import "./HintFinanceVault.sol";

contract HintFinanceFactory {

    mapping(address => address) public underlyingToVault;
    mapping(address => address) public vaultToUnderlying;
    mapping(address => bool) public rewardTokenWhitelist;

    uint256 public constant rewardDuration = 10 days;
    address public immutable owner = msg.sender;

    function modifyRewardTokenWhitelist(address rewardToken, bool ok) external {
        require(msg.sender == owner);
        rewardTokenWhitelist[rewardToken] = ok;
    }

    function createVault(address token) external returns (address) {
        require(underlyingToVault[token] == address(0));
        address vault = underlyingToVault[token] = address(new HintFinanceVault(token));
        vaultToUnderlying[vault] = token;
        return vault;
    }

    function addRewardToVault(address vault, address rewardToken) external {
        require(rewardTokenWhitelist[rewardToken]);
        require(vaultToUnderlying[vault] != address(0) && vaultToUnderlying[vault] != rewardToken);
        HintFinanceVault(vault).addReward(rewardToken, rewardDuration);
    }
}