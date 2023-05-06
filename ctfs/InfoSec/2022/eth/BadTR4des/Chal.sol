// SPDX-License-Identifier: UNLICENSED

// Challenge prepared for infosec CTF 2022

pragma solidity ^0.8.13;

import "./IUniswapV2Router.sol";
import "./IERC20.sol";

contract Chal {
    address private constant UNISWAP_V2_ROUTER = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;
    address private constant DAI = 0x6B175474E89094C44Da98b954EedeAC495271d0F;
    address private constant USDC = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;

    IUniswapV2Router private router = IUniswapV2Router(UNISWAP_V2_ROUTER);
    IERC20 private dai = IERC20(DAI);
    IERC20 private usdc = IERC20(USDC);

    mapping (address => uint) public balanceOf;

    constructor() {
        dai.approve(address(router), type(uint256).max);
        usdc.approve(address(router), type(uint256).max);
    }

    function depositUSDC(uint amountIn) public {
        bool success = usdc.transferFrom(msg.sender, address(this), amountIn);
        require(success);
        balanceOf[msg.sender] += amountIn;
    }

    function depositDAI(uint amountIn) public {
        bool success = dai.transferFrom(msg.sender, address(this), amountIn);
        require(success);
        balanceOf[msg.sender] += amountIn/10e12;
    }

    function withdrawUSDC(uint amountOut) public {
        require(balanceOf[msg.sender] >= amountOut);
        balanceOf[msg.sender] -= amountOut;

        if (usdc.balanceOf(address(this)) < amountOut) {
            address[] memory path;
            path = new address[](2);
            path[0] = DAI;
            path[1] = USDC;

            uint[] memory amounts = router.swapExactTokensForTokens(
                dai.balanceOf(address(this)),
                0,
                path,
                address(this),
                block.timestamp
            );
        }
        
        usdc.transfer(msg.sender, amountOut);
    }

    function withdrawDAI(uint amountOut) public {
        require(balanceOf[msg.sender] >= amountOut);
        balanceOf[msg.sender] -= amountOut;

        if (dai.balanceOf(address(this)) < amountOut*10e12) {
            address[] memory path;
            path = new address[](2);
            path[0] = USDC;
            path[1] = DAI;

            uint[] memory amounts = router.swapExactTokensForTokens(
                usdc.balanceOf(address(this)),
                0,
                path,
                address(this),
                block.timestamp
            );
        }
        
        dai.transfer(msg.sender, amountOut*10e12);
    }
}
