// SPDX-License-Identifier: MIT
pragma solidity 0.8.21;
import "./ERC20.sol";

contract RewardToken is ERC20 {
    constructor() ERC20("Reward Token", "RT") {
        _mint(msg.sender, 1e32);
    }
}

contract Challenge {
    /// Mapping from user ID to balance
    mapping (uint256 => UserInfo) public userInfo;
    
    /// Reward token
    RewardToken public rewardToken;

    /// Settings
    address public owner;
    uint256 public combinedMultiplier = 2;
    uint256 public timePerClaim = 1 days;

    constructor() {
        rewardToken = new RewardToken();
        owner = 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266; // in deployed challenge, this address is different!!!!
    }

    function isSolved() public view returns (bool) {
        return rewardToken.balanceOf(address(this)) == 0;
    }

    struct Action {
        uint8 _type; // 0 - initialize, 1 - mint duck, 2 - combine ducks
        uint256 timestamp; // timestamp of the action
        uint256 extraInfo; // can be used for duck level or reward receiver
    }

    struct UserInfo {
        bool initialized; // is user initialized
        uint256 lastProfitClaim; // timestamp
        uint256 profitPerSecond; // profit per second
        address rewardReceiver; // where to send the reward
        mapping (uint8 => uint256) ducks; // level => count
    }

    event MintDuck(uint256 userId, uint256 timestamp);
    event CombineDucks(uint256 userId, uint256 timestamp, uint8 duckLevel);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function.");
        _;
    }

    function checkpoint(uint256 userId, Action[] calldata actions) external onlyOwner {
        UserInfo storage info = userInfo[userId];
        for (uint256 i = 0; i < actions.length; i++) {
            Action memory action = actions[i];
            if (action._type == 0) {  // initialize account
                require(!info.initialized, "User is already initialized");
                info.initialized = true;
                info.rewardReceiver = address(uint160(action.extraInfo));
                info.lastProfitClaim = block.timestamp;
            }
            if (action._type == 1) {  // mint duck
                require(info.initialized, "User is not initialized");
                info.profitPerSecond += 1;
                info.ducks[0] += 1;
                emit MintDuck(userId, action.timestamp);
            }
            if (action._type == 2) { // combine ducks
                require(info.initialized, "User is not initialized");
                uint8 level = uint8(action.extraInfo);
                require(info.ducks[level - 1] >= 2, "Not enough ducks to combine");
                info.ducks[level - 1] -= 2;
                info.ducks[level] += 1;
                info.profitPerSecond += level * combinedMultiplier;
            } 
        }
        // claim profit every `timePerClaim` seconds
        if (info.lastProfitClaim + timePerClaim < block.timestamp) {
            uint256 timeSinceLastCheckpoint = block.timestamp - info.lastProfitClaim;
            rewardToken.transfer(info.rewardReceiver, timeSinceLastCheckpoint * info.profitPerSecond);
            info.lastProfitClaim = block.timestamp;
        }
    }

    function getDucks(uint256 userId) external view returns (uint256[12] memory) {
        UserInfo storage info = userInfo[userId];
        uint256[12] memory ducks;
        for (uint8 i = 0; i < 12; i++) { ducks[i] = info.ducks[i]; }
        return ducks;
    }

    function getProfitPerSecond(uint256 userId) external view returns (uint256) {
        return userInfo[userId].profitPerSecond;
    }

    function getRewardReceiver(uint256 userId) external view returns (address) {
        return userInfo[userId].rewardReceiver;
    }

    function updateSettings(address _owner, uint256 _combinedMultiplier, uint256 _timePerClaim) external onlyOwner {
        combinedMultiplier = _combinedMultiplier;
        owner = _owner;
        timePerClaim = _timePerClaim;
    }
}
