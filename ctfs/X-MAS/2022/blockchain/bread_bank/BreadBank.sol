// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.17;

import "./ERC20.sol";
import "./BankPairERC20.sol";

contract BreadBank {
    
    // @dev Allows a user to deposit the ERC20 underlying token into the bank.
    function createDepositToken(ERC20 _underlying, uint256 _amount) public returns(BankPairERC20){
        // Assure _underlying is not the BANK token.
        require(address(_underlying) != address(this), "BreadBank: Cannot deposit BANK token.");

        // Assure enough tokens have been transferred to the bank.
        require(_underlying.balanceOf(address(this)) >= _amount, "BreadBank: Not enough tokens have been deposited.");

        // Create a new bankpair token for the user.
        BankPairERC20 depositToken = new BankPairERC20(_underlying, _amount);

        // Mint the deposit token to the user.
        depositToken.mint(msg.sender, _amount);

        // Return the deposit token.
        return depositToken;
    }

    // @dev Allows a user to calculate the rewards they will receive for a given bank pair token.
    function calculateRewards(BankPairERC20 _bankPairToken) public view returns (uint256) {
        // Get the underlying token.
        ERC20 underlying = _bankPairToken.underlying();

        // Get the total supply of the bank pair token.
        uint256 totalBankPairSupply = _bankPairToken.totalSupply();

        // Get the total supply of the underlying token.
        uint256 underlyingTotalSupply = underlying.totalSupply();

        // Get the balance of the underlying token.
        uint256 underlyingBalance = underlying.balanceOf(address(this));

        // Calculate the rewards.
        uint256 rewards = (underlyingBalance * _bankPairToken.balanceOf(msg.sender)) / (underlyingTotalSupply * totalBankPairSupply);

        return rewards;
    }

    // @dev Allows a user to receive rewards for a given bank pair token.
    function issueRewards(BankPairERC20 _bankPairToken) public {
        // Get the rewards.
        uint256 rewards = calculateRewards(_bankPairToken);

        // Mint the rewards to the user.
        _bankPairToken.mint(msg.sender, rewards);
    }

    // @dev Allows a user to redeem their bank pair token for the underlying token.
    function redeem(BankPairERC20 _bankPairToken, uint256 _amount) public {
        
        // Assure _amount is not 0.
        require(_amount != 0, "BreadBank: Cannot redeem 0 tokens.");

        // Assure the user has enough bank pair tokens.
        require(_bankPairToken.balanceOf(msg.sender) >= _amount, "BreadBank: Not enough tokens have been deposited.");

        // Get the underlying token.
        ERC20 underlying = _bankPairToken.underlying();

        // Burn the bank pair token.
        _bankPairToken.burn(msg.sender, _amount);

        // Transfer the underlying token to the user.
        underlying.transfer(msg.sender, _amount);
    }


}