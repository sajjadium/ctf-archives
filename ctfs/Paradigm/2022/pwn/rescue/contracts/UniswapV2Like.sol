// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.16;

interface UniswapV2RouterLike {
	function swapExactTokensForTokens(
        uint amountIn,
        uint amountOutMin,
        address[] calldata path,
        address to,
        uint deadline
    ) external returns (uint[] memory amounts);

	function addLiquidity(
        address tokenA,
        address tokenB,
        uint amountADesired,
        uint amountBDesired,
        uint amountAMin,
        uint amountBMin,
        address to,
        uint deadline
    ) external returns (uint amountA, uint amountB, uint liquidity);
}

interface UniswapV2PairLike {
    function token0() external returns (address);
    function token1() external returns (address);
}