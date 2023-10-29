// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.19;

import "./uniswap-updated/INonfungiblePositionManager.sol";

/**
 * @dev Interface of the MigrateV3NFT contract
 */
interface IMigrateV3NFT {
    function migrate(uint256 lockId, INonfungiblePositionManager nftPositionManager, uint256 tokenId)
        external
        returns (bool);
}
