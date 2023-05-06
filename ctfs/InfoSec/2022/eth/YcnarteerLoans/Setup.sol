// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.16;

import "./EasyFactory.sol";

interface UniswapV2Router {
    function swapExactETHForTokens(uint amountOutMin, address[] memory path, address to, uint deadline) external payable;
}

contract Setup {

    address[3] public underlyingTokens = [
        0x89Ab32156e46F46D02ade3FEcbe5Fc4243B9AAeD,
        0x3845badAde8e6dFF049820680d1F14bD3903a5d0,
        0xfF20817765cB7f73d4bde2e66e067E58D11095C2
    ];

    address[3] public rewardTokens = [
        0xdAC17F958D2ee523a2206206994597C13D831ec7,
        0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48,
        0x6B175474E89094C44Da98b954EedeAC495271d0F
    ];

    uint256[3] public initialUnderlyingBalances;
    EasyFactory public easyFactory = new EasyFactory();

    constructor() payable {
        
        UniswapV2Router router = UniswapV2Router(0xf164fC0Ec4E93095b804a4795bBe1e041497b92a);
        address weth = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
        address[] memory path = new address[](2);
        path[0] = weth;

        for (uint256 i = 0; i < underlyingTokens.length; ++i) {
            path[1] = underlyingTokens[i];
            router.swapExactETHForTokens{value: 10 ether}(0, path, address(this), block.timestamp);
            
            address vault = easyFactory .createVault(underlyingTokens[i]);
            ERC20(underlyingTokens[i]).approve(vault, type(uint256).max);
            EasyVault(vault).deposit(ERC20(underlyingTokens[i]).balanceOf(address(this)));
            initialUnderlyingBalances[i] = ERC20(underlyingTokens[i]).balanceOf(vault);
        }

        for (uint256 i = 0; i < rewardTokens.length; ++i) {
            easyFactory .modifyRewardTokenWhitelist(rewardTokens[i], true);
        }
    }
    
    function isSolved() public view returns (bool) {
        for (uint256 i = 0; i < underlyingTokens.length; ++i) {
            address vault = easyFactory .underlyingToVault(underlyingTokens[i]);
            uint256 vaultUnderlyingBalance = ERC20(underlyingTokens[i]).balanceOf(vault);
            if (vaultUnderlyingBalance > initialUnderlyingBalances[i] / 100) return false;
        }
        return true;
    }
}