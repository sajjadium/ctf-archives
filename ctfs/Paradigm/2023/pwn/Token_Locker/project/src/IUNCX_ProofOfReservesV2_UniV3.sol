// SPDX-License-Identifier: UNLICENSED
// ALL RIGHTS RESERVED
// UNCX by SDDTech reserves all rights on this code. You may not copy these contracts.

pragma solidity 0.8.19;

import "./uniswap-updated/INonfungiblePositionManager.sol";

/**
 * @dev Interface of the UNCX UniswapV3 Liquidity Locker
 */
interface IUNCX_ProofOfReservesV2_UniV3 {
    struct FeeStruct {
        string name; // name by which the fee is accessed
        uint256 lpFee; // 100 = 1%, 10,000 = 100%
        uint256 collectFee; // 100 = 1%, 10,000 = 100%
        uint256 flatFee; // in amount tokens
        address flatFeeToken; // address(0) = ETH otherwise ERC20 address expected
    }

    struct Lock {
        uint256 lock_id; // unique nonce per lock
        INonfungiblePositionManager nftPositionManager; // the nft position manager of the uniswap fork
        address pool; // the pool address
        uint256 nft_id; // the nft token id of the nft belonging to the nftPositionManager (there could be two nfts with id = 1, belonging to different amm forks and position managers)
        address owner; // the owner who can collect and withdraw
        address pendingOwner; //  two step process ownership transfer, the pending owner must accept ownership to own the lock
        address additionalCollector; // an additional address allowed to call collect (ideal for contracts to auto collect without having to use owner)
        address collectAddress; // The address to which automatic collections are sent
        uint256 unlockDate; // unlock date of the lock in seconds
        uint16 countryCode; // the country code of the locker / business
        uint256 ucf; // collect fee
    }

    struct LockParams {
        INonfungiblePositionManager nftPositionManager; // the NFT Position manager of the Uniswap V3 fork
        uint256 nft_id; // the nft token_id
        address dustRecipient; // receiver of dust tokens which do not fit into liquidity and initial collection fees
        address owner; // owner of the lock
        address additionalCollector; // an additional address allowed to call collect (ideal for contracts to auto collect without having to use owner)
        address collectAddress; // The address to which automatic collections are sent
        uint256 unlockDate; // unlock date of the lock in seconds
        uint16 countryCode; // the country code of the locker / business
        string feeName; // The fee name key you wish to accept, use "DEFAULT" if in doubt
        bytes[] r; // use an empty array => []
    }

    struct Position {
        uint96 nonce;
        address operator;
        address token0;
        address token1;
        uint24 fee;
        int24 tickLower;
        int24 tickUpper;
        uint128 liquidity;
        uint256 feeGrowthInside0LastX128;
        uint256 feeGrowthInside1LastX128;
        uint128 tokensOwed0;
        uint128 tokensOwed1;
    }

    // User functions
    function lock(LockParams calldata params) external payable returns (uint256 lockId);
    function collect(uint256 lockId, address recipient, uint128 amount0Max, uint128 amount1Max)
        external
        returns (uint256 amount0, uint256 amount1, uint256 fee0, uint256 fee1);
    function withdraw(uint256 lockId, address receiver) external;
    function migrate(uint256 lockId) external;
    function relock(uint256 lockId, uint256 unlockDate) external;
    function setAdditionalCollector(uint256 lockId, address additionalCollector) external;
    function setCollectAddress(uint256 lockId, address collectAddress) external;
    function transferLockOwnership(uint256 lockId, address newOwner) external;
    function acceptLockOwnership(uint256 lockId) external;
    function decreaseLiquidity(uint256 lockId, INonfungiblePositionManager.DecreaseLiquidityParams calldata params)
        external
        payable
        returns (uint256 amount0, uint256 amount1);
    function increaseLiquidity(uint256 lockId, INonfungiblePositionManager.IncreaseLiquidityParams calldata params)
        external
        payable
        returns (uint128 liquidity, uint256 amount0, uint256 amount1);

    // Admin functions
    function setMigrator(address migrator) external;
    function setUCF(uint256 lockId, uint256 ucf) external;
    function setMigrateInContract(address migrateInContract) external;

    // Getters
    function getLocksLength() external view returns (uint256);
    function getLock(uint256 lockId) external view returns (Lock memory lock);

    function getNumUserLocks(address user) external view returns (uint256 numLocks);
    function getUserLockAtIndex(address user, uint256 index) external view returns (Lock memory lock);

    function getFee(string memory name) external view returns (FeeStruct memory);
    function getAmountsForLiquidity(int24 currentTick, int24 tickLower, int24 tickHigher, uint128 liquidity)
        external
        pure
        returns (uint256 amount0, uint256 amount1);

    // Events
    event onLock(
        uint256 lock_id,
        address nftPositionManager,
        uint256 nft_id,
        address owner,
        address additionalCollector,
        address collectAddress,
        uint256 unlockDate,
        uint16 countryCode,
        uint256 collectFee,
        address poolAddress,
        Position position
    );

    event onWithdraw(uint256 lock_id, address owner, address receiver);

    event onLockOwnershipTransferStarted(uint256 lockId, address currentOwner, address pendingOwner);

    event onTransferLockOwnership(uint256 lockId, address oldOwner, address newOwner);

    event onMigrate(uint256 lockId);

    event onSetAdditionalCollector(uint256 lockId, address additionalCollector);

    event onSetCollectAddress(uint256 lockId, address collectAddress);

    event onSetMigrator(address migrator);

    event onRelock(uint256 lockId, uint256 unlockDate);

    event onIncreaseLiquidity(uint256 lockId);

    event onDecreaseLiquidity(uint256 lockId);

    event onRemoveFee(bytes32 nameHash);

    event onAddFee(
        bytes32 nameHash, string name, uint256 lpFee, uint256 collectFee, uint256 flatFee, address flatFeeToken
    );

    event onEditFee(
        bytes32 nameHash, string name, uint256 lpFee, uint256 collectFee, uint256 flatFee, address flatFeeToken
    );

    event onSetUCF(uint256 lockId, uint256 ucf);
}
