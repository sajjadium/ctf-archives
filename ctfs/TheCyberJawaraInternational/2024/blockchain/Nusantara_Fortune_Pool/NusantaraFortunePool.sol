// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Ownable.sol";

contract NusantaraFortunePool is Ownable {
    mapping(address => uint256) public stakes;
    mapping(address => bool) public hasStaked;
    mapping(address => uint256) public rewards;
    uint256 public rewardPercentage;
    uint256 public constant MAX_REWARD_PERCENTAGE = 4; // 4% max reward
    bool public isActive;

    constructor(uint256 _rewardPercentage) {
        require(_rewardPercentage <= MAX_REWARD_PERCENTAGE, "Reward percentage too high");
        rewardPercentage = _rewardPercentage;
        isActive = false;
    }

    // Function to activate the pool
    function activate() external onlyOwner {
        isActive = true;
    }

    // Function to deactivate the pool
    function deactivate() external onlyOwner {
        isActive = false;
    }

    // Stake Ether into the pool
    function stake(address user, uint256 amount, bool isRealOwner) external payable onlyOwner {
        require(isActive, "Pool is not active");
        require(amount > 0, "Cannot stake 0");
        require(isRealOwner || amount <= 1_000_000, "Cannot stake more than 1_000_000 ether");
        require(!hasStaked[user], "Already staked");
        stakes[user] = amount;
        hasStaked[user] = true;
    }

    // Calculate reward without transferring
    function distributeReward(address user) external onlyOwner returns (uint256) {
        require(isActive, "Pool is not active");
        require(stakes[user] > 0, "No stake found");

        uint256 reward = stakes[user] * rewardPercentage / 100;
        rewards[user] = reward;
        return reward;
    }

    // Unstake and return the staked amount
    function unstake(address user) external onlyOwner returns (uint256) {
        require(isActive, "Pool is not active");
        require(stakes[user] > 0, "No stake found");
        
        uint256 stakedAmount = stakes[user];
        stakes[user] = 0;
        
        return stakedAmount;
    }

    // Get the reward for a user, can be called by anyone
    function getReward(address user) external view returns (uint256) {
        return rewards[user];
    }

    // Get the status of the pool
    function getStatus() external view returns (bool) {
        return isActive;
    }
}