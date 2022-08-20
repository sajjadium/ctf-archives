// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.16;

interface ERC20Like {
    function transfer(address dst, uint qty) external returns (bool);
    function transferFrom(address src, address dst, uint qty) external returns (bool);
    function approve(address dst, uint qty) external returns (bool);
    function balanceOf(address who) external view returns (uint);
}

interface IHintFinanceFlashloanReceiver {
    function onHintFinanceFlashloan(
        address token,
        address factory,
        uint256 amount,
        bool isUnderlyingOrReward,
        bytes memory data
    ) external;
}

contract HintFinanceVault {

    /* ========== STATE VARIABLES ========== */

    struct Reward {
        uint256 rewardsDuration;
        uint256 periodFinish;
        uint256 rewardRate;
        uint256 lastUpdateTime;
        uint256 rewardPerTokenStored;
    }

    mapping(address => Reward) public rewardData;
    address[] public rewardTokens;

    mapping(address => mapping(address => uint256)) public userRewardPerTokenPaid;
    mapping(address => mapping(address => uint256)) public rewards;

    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;

    address public immutable factory;
    address public immutable underlyingToken;

    bool locked = false;

    /* ========== CONSTRUCTOR ========== */

    constructor(address _underlyingToken) {
        underlyingToken = _underlyingToken;
        factory = msg.sender;
    }

    /* ========== RESTRICTED FUNCTIONS ========== */

    function addReward(address rewardToken, uint256 rewardDuration) external {
        require(msg.sender == factory);
        require(rewardData[rewardToken].rewardsDuration == 0);
        rewardTokens.push(rewardToken);
        rewardData[rewardToken].rewardsDuration = rewardDuration;
    }

    /* ========== VIEWS ========== */

    function lastTimeRewardApplicable(address rewardToken) public view returns (uint256) {
        if (block.timestamp < rewardData[rewardToken].periodFinish) {
            return block.timestamp;
        } else {
            return rewardData[rewardToken].periodFinish;
        }
    }

    function rewardPerToken(address rewardToken) public view returns (uint256) {
        if (totalSupply == 0) return 0;
        uint256 newTime = lastTimeRewardApplicable(rewardToken) - rewardData[rewardToken].lastUpdateTime;
        uint256 newAccumulated = newTime * rewardData[rewardToken].rewardRate / totalSupply;
        return rewardData[rewardToken].rewardPerTokenStored + newAccumulated;
    }

    function earned(address account, address rewardToken) public view returns (uint256) {
        uint256 newAccumulated = balanceOf[account] * (rewardPerToken(rewardToken) - userRewardPerTokenPaid[account][rewardToken]);
        return rewards[account][rewardToken] + newAccumulated;
    }

    /* ========== MUTATIVE FUNCTIONS ========== */

    function provideRewardTokens(address rewardToken, uint256 amount) public updateReward(address(0)) {
        require(rewardData[rewardToken].rewardsDuration != 0);
        _updateRewardRate(rewardToken, amount);
        ERC20Like(rewardToken).transferFrom(msg.sender, address(this), amount);
    }

    function _updateRewardRate(address rewardToken, uint256 amount) internal {
        if (block.timestamp >= rewardData[rewardToken].periodFinish) {
            rewardData[rewardToken].rewardRate = amount / rewardData[rewardToken].rewardsDuration;
        } else {
            uint256 remaining = rewardData[rewardToken].periodFinish - block.timestamp;
            uint256 leftover = remaining * rewardData[rewardToken].rewardRate;
            rewardData[rewardToken].rewardRate = (amount + leftover) / rewardData[rewardToken].rewardsDuration;
        }
        rewardData[rewardToken].lastUpdateTime = block.timestamp;
        rewardData[rewardToken].periodFinish = block.timestamp + rewardData[rewardToken].rewardsDuration;
    }

    function getRewards() external updateReward(msg.sender) {
        for (uint i; i < rewardTokens.length; i++) {
            address rewardToken = rewardTokens[i];
            uint256 reward = rewards[msg.sender][rewardToken];
            if (reward > 0) {
                rewards[msg.sender][rewardToken] = 0;
                ERC20Like(rewardToken).transfer(msg.sender, reward);
            }
        }
    }

    function deposit(uint256 amount) external updateReward(msg.sender) returns (uint256) {
        uint256 bal = ERC20Like(underlyingToken).balanceOf(address(this));
        uint256 shares = totalSupply == 0 ? amount : amount * totalSupply / bal;
        ERC20Like(underlyingToken).transferFrom(msg.sender, address(this), amount);
        totalSupply += shares;
        balanceOf[msg.sender] += shares;
        return shares;
    }

    function withdraw(uint256 shares) external updateReward(msg.sender) returns (uint256) {
        uint256 bal = ERC20Like(underlyingToken).balanceOf(address(this));
        uint256 amount = shares * bal / totalSupply;
        ERC20Like(underlyingToken).transfer(msg.sender, amount);
        totalSupply -= shares;
        balanceOf[msg.sender] -= shares;
        return amount;
    }

    function flashloan(address token, uint256 amount, bytes calldata data) external updateReward(address(0)) {
        uint256 supplyBefore = totalSupply;
        uint256 balBefore = ERC20Like(token).balanceOf(address(this));
        bool isUnderlyingOrReward = token == underlyingToken || rewardData[token].rewardsDuration != 0;

        ERC20Like(token).transfer(msg.sender, amount);
        IHintFinanceFlashloanReceiver(msg.sender).onHintFinanceFlashloan(token, factory, amount, isUnderlyingOrReward, data);

        uint256 balAfter = ERC20Like(token).balanceOf(address(this));
        uint256 supplyAfter = totalSupply;

        require(supplyBefore == supplyAfter);
        if (isUnderlyingOrReward) {
            uint256 extra = balAfter - balBefore;
            if (extra > 0 && token != underlyingToken) {
                _updateRewardRate(token, extra);
            }
        } else {
            require(balAfter == balBefore); // don't want random tokens to get stuck
        }
    }

    /* ========== MODIFIERS ========== */

    modifier updateReward(address account) {
        for (uint i; i < rewardTokens.length; i++) {
            address token = rewardTokens[i];
            rewardData[token].rewardPerTokenStored = rewardPerToken(token);
            rewardData[token].lastUpdateTime = lastTimeRewardApplicable(token);
            if (account != address(0)) {
                rewards[account][token] = earned(account, token);
                userRewardPerTokenPaid[account][token] = rewardData[token].rewardPerTokenStored;
            }
        }
        _;
    }
}


