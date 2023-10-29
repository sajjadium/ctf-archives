// SPDX-License-Identifier: UNLICENSED
pragma solidity =0.7.6;

import '../libraries/PositionValue.sol';
import '../interfaces/INonfungiblePositionManager.sol';

contract PositionValueTest {
    function total(
        INonfungiblePositionManager nft,
        uint256 tokenId,
        uint160 sqrtRatioX96
    ) external view returns (uint256 amount0, uint256 amount1) {
        return PositionValue.total(nft, tokenId, sqrtRatioX96);
    }

    function principal(
        INonfungiblePositionManager nft,
        uint256 tokenId,
        uint160 sqrtRatioX96
    ) external view returns (uint256 amount0, uint256 amount1) {
        return PositionValue.principal(nft, tokenId, sqrtRatioX96);
    }

    function fees(INonfungiblePositionManager nft, uint256 tokenId)
        external
        view
        returns (uint256 amount0, uint256 amount1)
    {
        return PositionValue.fees(nft, tokenId);
    }

    function totalGas(
        INonfungiblePositionManager nft,
        uint256 tokenId,
        uint160 sqrtRatioX96
    ) external view returns (uint256) {
        uint256 gasBefore = gasleft();
        PositionValue.total(nft, tokenId, sqrtRatioX96);
        return gasBefore - gasleft();
    }

    function principalGas(
        INonfungiblePositionManager nft,
        uint256 tokenId,
        uint160 sqrtRatioX96
    ) external view returns (uint256) {
        uint256 gasBefore = gasleft();
        PositionValue.principal(nft, tokenId, sqrtRatioX96);
        return gasBefore - gasleft();
    }

    function feesGas(INonfungiblePositionManager nft, uint256 tokenId) external view returns (uint256) {
        uint256 gasBefore = gasleft();
        PositionValue.fees(nft, tokenId);
        return gasBefore - gasleft();
    }
}
