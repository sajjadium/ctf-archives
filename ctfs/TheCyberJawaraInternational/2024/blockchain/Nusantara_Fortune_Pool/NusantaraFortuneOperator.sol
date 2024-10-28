// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./NusantaraFortunePool.sol";
import "./Ownable.sol";

contract NusantaraFortuneOperator is Ownable {
    mapping(bytes32 => address) private _fortunePools;
    mapping(bytes32 => uint256) private _lastVerified;

    // Deploy a new NusantaraFortunePool
    function deployNewPool(uint256 _rewardPercentage) external onlyOwner returns (bytes32, address) {
        NusantaraFortunePool newPool = new NusantaraFortunePool(_rewardPercentage);
        bytes32 poolId = keccak256(abi.encodePacked(address(newPool)));
        require(_fortunePools[poolId] == address(0), "Pool exist");
        _fortunePools[poolId] = address(newPool);
        return (poolId, address(newPool));
    }

    function activatePool(bytes32 poolId, address pool) external onlyOwner {
        require(keccak256(abi.encodePacked(pool)) == poolId, "Pool ID mismatch");
        require(_fortunePools[poolId] == address(pool), "Pool ID mismatch");
        NusantaraFortunePool fortunePool = NusantaraFortunePool(pool);
        require(!fortunePool.getStatus(), "Pool is already active");
        fortunePool.activate();
    }

    function deactivatePool(bytes32 poolId, address pool) external onlyOwner {
        require(keccak256(abi.encodePacked(pool)) == poolId, "Pool ID mismatch");
        require(_fortunePools[poolId] == address(pool), "Pool ID mismatch");
        NusantaraFortunePool fortunePool = NusantaraFortunePool(pool);
        require(fortunePool.getStatus(), "Pool is already non-active");
        fortunePool.deactivate();
    }

    // Verify the pool periodically by ensuring it is active
    function verifyPool(bytes32 poolId, address pool) external {
        require(keccak256(abi.encodePacked(pool)) == poolId, "Pool ID mismatch");
        require(_fortunePools[poolId] == address(pool), "Pool ID mismatch");

        if (_lastVerified[poolId] == 0 || _lastVerified[poolId] + 1 days < block.timestamp) {
            require(_verifyPool(poolId, pool), "Pool is not active, please ask admin to activate");
        }

        _lastVerified[poolId] = block.timestamp;
    }

    // Withdraw staked amount from a specific pool
    function withdrawStaked(bytes32 poolId, address pool) external {
        require(keccak256(abi.encodePacked(pool)) == poolId, "Pool ID mismatch");

        // Disallow verification on-the-fly in order to:
        // - Discourage user from withdrawing their money from our pool for the sake of retention.
        // - Encourage user to either contribute or claim reward for user retention.
        require(_lastVerified[poolId] == 0 || _lastVerified[poolId] + 1 days >= block.timestamp, "Pool isn't verified yet");

        NusantaraFortunePool fortunePool = NusantaraFortunePool(pool);
        
        // Call the pool to unstake and get the staked amount
        uint256 stakedAmount = fortunePool.unstake(msg.sender);
        
        // Transfer the staked amount back to the user
        (bool success, ) = msg.sender.call{value: stakedAmount}("");
        require(success, "Staked amount transfer failed");
    }

    // Stake Ether into a specific pool
    function contributeToPool(bytes32 poolId, address pool) external payable {
        require(keccak256(abi.encodePacked(pool)) == poolId, "Pool ID mismatch");

        // Verify pool on-the-fly in order to:
        // - Encourage user to contribute more to the pool.
        if (_lastVerified[poolId] == 0 || _lastVerified[poolId] + 1 days < block.timestamp) {
            require(_verifyPool(poolId, pool), "Pool is not active, please ask admin to activate");
        } else if (_fortunePools[poolId] != pool) {
            revert("Pool does not exist");
        }

        require(msg.value > 0, "Cannot stake 0");

        // Stake directly into the NusantaraFortunePool
        NusantaraFortunePool fortunePool = NusantaraFortunePool(pool);
        fortunePool.stake(msg.sender, msg.value, msg.sender == owner());
    }

    // Claim reward from a specific pool
    function claimPoolReward(bytes32 poolId, address pool) external {
        require(keccak256(abi.encodePacked(pool)) == poolId, "Pool ID mismatch");

        // Verify pool on-the-fly in order to:
        // - Encourage user to claim reward for retention.
        // - Encourage user to contribute more due to the claimed reward.
        if (_lastVerified[poolId] == 0 || _lastVerified[poolId] + 1 days < block.timestamp) {
            require(_verifyPool(poolId, pool), "Pool is not active, please ask admin to activate");
        } else if (_fortunePools[poolId] == address(0)) {
            revert("Pool does not exist");
        }

        NusantaraFortunePool fortunePool = NusantaraFortunePool(pool);
        
        // Call the pool to distribute the reward
        uint256 reward = fortunePool.distributeReward(msg.sender);
        
        // Transfer the reward to the user
        (bool success, ) = msg.sender.call{value: reward}("");
        require(success, "Reward transfer failed");
    }

    // Internal function to verify and get the pool status
    function _verifyPool(bytes32 poolId, address pool) internal view returns (bool) {
        return NusantaraFortunePool(pool).getStatus();
    }

    // Fallback function to accept Ether
    receive() external payable {}
}