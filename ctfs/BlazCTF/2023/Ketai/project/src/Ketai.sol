// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./ERC20.sol";
import "./PancakeSwap/PancakeRouter.sol";
import "./PancakeSwap/PancakePair.sol";

contract Ketai is ERC20, Ownable {
    IPancakePair public pair;
    IERC20 public usdt;
    IPancakeRouter02 public router;

    uint256 public tradeFee = 30;

    address[] public lpProviders;

    constructor() ERC20("Ketai", "KT") {
        _mint(msg.sender, 10000000 * 1e18);
    }

    function setTradingInfo(address _usdt, address _pair, address _router) public onlyOwner {
        usdt = IERC20(_usdt);
        pair = IPancakePair(_pair);
        router = IPancakeRouter02(_router);
        // investor 1 (Binance), thank you
        lpProviders.push(0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8);
        // investor 2 (FTX), thank you
        lpProviders.push(0x50D1c9771902476076eCFc8B2A83Ad6b9355a4c9);
        // @shou: ftx bankrupcy
        // delete lpProviders[1];
    }

    function _transfer(
        address from,
        address to,
        uint256 amount
    ) internal override {
        require(from != address(0), "ERC20: transfer from the zero address");
        require(amount > 0, "ERC20: wrong amount");

        // if you are buying / selling token, you need to pay fee
        if (from == address(pair) || to == address(pair)) {
            uint256 fee = amount * tradeFee / 100;
            _balances[from] -= amount;
            _balances[to] += amount - fee;
            _balances[address(this)] += fee * lpProviders.length;
        } else {
            _balances[from] -= amount;
            _balances[to] += amount;
        }
    }

    // sell token to usdt via pancake router
    function sellToUSDT(uint amount, address rewardTarget) private {
        address[] memory path = new address[](2);
        _approve(address(this), address(router), amount);
        path[0] = address(this);
        path[1] = address(usdt);
        router.swapExactTokensForTokensSupportingFeeOnTransferTokens(
            amount,
            0,
            path,
            rewardTarget,
            block.timestamp
        );
    }

    // sell token to usdt via pancake router and distribute usdt to lpProviders
    function distributeReward() public {
        uint256 rewardToken = balanceOf(address(this));
        for (uint256 i = 0; i < lpProviders.length; i++) {
            // sellToUSDT(rewardToken / lpProviders.length, lpProviders[i]);
            // @shou: lol fuck, i am not going to pay binance
            sellToUSDT(rewardToken / lpProviders.length, owner());
        }
    }
}

