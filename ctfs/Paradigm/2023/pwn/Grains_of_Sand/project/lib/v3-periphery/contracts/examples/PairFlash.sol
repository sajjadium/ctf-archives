// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity =0.7.6;
pragma abicoder v2;

import '@uniswap/v3-core/contracts/interfaces/callback/IUniswapV3FlashCallback.sol';
import '@uniswap/v3-core/contracts/libraries/LowGasSafeMath.sol';

import '../base/PeripheryPayments.sol';
import '../base/PeripheryImmutableState.sol';
import '../libraries/PoolAddress.sol';
import '../libraries/CallbackValidation.sol';
import '../libraries/TransferHelper.sol';
import '../interfaces/ISwapRouter.sol';

/// @title Flash contract implementation
/// @notice An example contract using the Uniswap V3 flash function
contract PairFlash is IUniswapV3FlashCallback, PeripheryPayments {
    using LowGasSafeMath for uint256;
    using LowGasSafeMath for int256;

    ISwapRouter public immutable swapRouter;

    constructor(
        ISwapRouter _swapRouter,
        address _factory,
        address _WETH9
    ) PeripheryImmutableState(_factory, _WETH9) {
        swapRouter = _swapRouter;
    }

    // fee2 and fee3 are the two other fees associated with the two other pools of token0 and token1
    struct FlashCallbackData {
        uint256 amount0;
        uint256 amount1;
        address payer;
        PoolAddress.PoolKey poolKey;
        uint24 poolFee2;
        uint24 poolFee3;
    }

    /// @param fee0 The fee from calling flash for token0
    /// @param fee1 The fee from calling flash for token1
    /// @param data The data needed in the callback passed as FlashCallbackData from `initFlash`
    /// @notice implements the callback called from flash
    /// @dev fails if the flash is not profitable, meaning the amountOut from the flash is less than the amount borrowed
    function uniswapV3FlashCallback(
        uint256 fee0,
        uint256 fee1,
        bytes calldata data
    ) external override {
        FlashCallbackData memory decoded = abi.decode(data, (FlashCallbackData));
        CallbackValidation.verifyCallback(factory, decoded.poolKey);

        address token0 = decoded.poolKey.token0;
        address token1 = decoded.poolKey.token1;

        // profitability parameters - we must receive at least the required payment from the arbitrage swaps
        // exactInputSingle will fail if this amount not met
        uint256 amount0Min = LowGasSafeMath.add(decoded.amount0, fee0);
        uint256 amount1Min = LowGasSafeMath.add(decoded.amount1, fee1);

        // call exactInputSingle for swapping token1 for token0 in pool with fee2
        TransferHelper.safeApprove(token1, address(swapRouter), decoded.amount1);
        uint256 amountOut0 =
            swapRouter.exactInputSingle(
                ISwapRouter.ExactInputSingleParams({
                    tokenIn: token1,
                    tokenOut: token0,
                    fee: decoded.poolFee2,
                    recipient: address(this),
                    deadline: block.timestamp,
                    amountIn: decoded.amount1,
                    amountOutMinimum: amount0Min,
                    sqrtPriceLimitX96: 0
                })
            );

        // call exactInputSingle for swapping token0 for token 1 in pool with fee3
        TransferHelper.safeApprove(token0, address(swapRouter), decoded.amount0);
        uint256 amountOut1 =
            swapRouter.exactInputSingle(
                ISwapRouter.ExactInputSingleParams({
                    tokenIn: token0,
                    tokenOut: token1,
                    fee: decoded.poolFee3,
                    recipient: address(this),
                    deadline: block.timestamp,
                    amountIn: decoded.amount0,
                    amountOutMinimum: amount1Min,
                    sqrtPriceLimitX96: 0
                })
            );

        // pay the required amounts back to the pair
        if (amount0Min > 0) pay(token0, address(this), msg.sender, amount0Min);
        if (amount1Min > 0) pay(token1, address(this), msg.sender, amount1Min);

        // if profitable pay profits to payer
        if (amountOut0 > amount0Min) {
            uint256 profit0 = amountOut0 - amount0Min;
            pay(token0, address(this), decoded.payer, profit0);
        }
        if (amountOut1 > amount1Min) {
            uint256 profit1 = amountOut1 - amount1Min;
            pay(token1, address(this), decoded.payer, profit1);
        }
    }

    //fee1 is the fee of the pool from the initial borrow
    //fee2 is the fee of the first pool to arb from
    //fee3 is the fee of the second pool to arb from
    struct FlashParams {
        address token0;
        address token1;
        uint24 fee1;
        uint256 amount0;
        uint256 amount1;
        uint24 fee2;
        uint24 fee3;
    }

    /// @param params The parameters necessary for flash and the callback, passed in as FlashParams
    /// @notice Calls the pools flash function with data needed in `uniswapV3FlashCallback`
    function initFlash(FlashParams memory params) external {
        PoolAddress.PoolKey memory poolKey =
            PoolAddress.PoolKey({token0: params.token0, token1: params.token1, fee: params.fee1});
        IUniswapV3Pool pool = IUniswapV3Pool(PoolAddress.computeAddress(factory, poolKey));
        // recipient of borrowed amounts
        // amount of token0 requested to borrow
        // amount of token1 requested to borrow
        // need amount 0 and amount1 in callback to pay back pool
        // recipient of flash should be THIS contract
        pool.flash(
            address(this),
            params.amount0,
            params.amount1,
            abi.encode(
                FlashCallbackData({
                    amount0: params.amount0,
                    amount1: params.amount1,
                    payer: msg.sender,
                    poolKey: poolKey,
                    poolFee2: params.fee2,
                    poolFee3: params.fee3
                })
            )
        );
    }
}
