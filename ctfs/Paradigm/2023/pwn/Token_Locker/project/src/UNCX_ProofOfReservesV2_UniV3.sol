// SPDX-License-Identifier: UNLICENSED
// ALL RIGHTS RESERVED
// UNCX by SDDTech reserves all rights on this code. You may not copy these contracts.

pragma solidity 0.8.19;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721Receiver.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable2Step.sol";
import "@openzeppelin/contracts/utils/structs/EnumerableSet.sol";

import "@uniswap/v3-core/contracts/interfaces/IUniswapV3Factory.sol";
import "@uniswap/v3-core/contracts/interfaces/IUniswapV3Pool.sol";
import "@uniswap/v3-periphery/contracts/libraries/TransferHelper.sol";

import "./uniswap-updated/TickMath.sol";
import "./uniswap-updated/LiquidityAmounts.sol";
import "./uniswap-updated/INonfungiblePositionManager.sol";
import "./ICountryList.sol";
import "./IMigrateV3NFT.sol";
import "./IUNCX_ProofOfReservesV2_UniV3.sol";

/*
    Version 2.0
    
    The UNCX Proof of Reserves V3 Contract locks any exact fork of Uniswap V3's liquidity NFT's in this contract.
    Proof of reserves means a user is aware that a pools liquidity cannot be removed until the time lock expires.
    Proof of reserves prevents hacks of founders wallets from comprimising this important aspect of their tokens ecosystem.

    Since liquidity means so much to all ecosystem participants, this contract converts a UniV3 position to full range, from the absolute 
    minimum lowerTick to the absolute maximum upperTick, creating a reliable pool where tokens will be tradeable at any price.

    Lock owners are still free to collect fees as they please, and add liquidity to their position, while the liquidity remains locked.

    You can also still view your NFT and its metrics on uniswap while it is locked. e.g. https://app.uniswap.org/#/pools/69
*/

interface IFeeResolver {
    function useFee(bytes[] memory r, address sender)
        external
        returns (IUNCX_ProofOfReservesV2_UniV3.FeeStruct memory fee);
}

contract UNCX_ProofOfReservesV2_UniV3 is
    IUNCX_ProofOfReservesV2_UniV3,
    Ownable2Step,
    IERC721Receiver,
    ReentrancyGuard
{
    using EnumerableSet for EnumerableSet.UintSet;
    using EnumerableSet for EnumerableSet.Bytes32Set;

    mapping(bytes32 => FeeStruct) private FEES; // map keccak(fee_name) to fee struct e.g. keccak256("DEFAULT") => FeeStruct
    EnumerableSet.Bytes32Set private FEE_LOOKUP; // contains keccak(feeName)

    IFeeResolver public FEE_RESOLVER; // Resolve R fees

    address public AUTO_COLLECT_ACCOUNT; // account controlled by UNCX to auto collect fees if a fee option involving collection fees was accepted
    address payable public FEE_ADDR_LP; // LP fee destination
    address payable public FEE_ADDR_COLLECT; // collect fee destination
    uint256 public constant FEE_DENOMINATOR = 10000; // denominator for all fees

    ICountryList public COUNTRY_LIST;
    IMigrateV3NFT public MIGRATOR; // migrate to future amm versions while liquidity remains locked
    address public MIGRATE_IN; // address of the migration in contract
    uint256 public NONCE = 0; // incremental lock nonce counter, this is the unique ID for the next lock

    // If a locks unlock date is set to ETERNAL_LOCK the lock is eternal and not ever withdrawable.
    // It can however be migrated by the owner to future AMMS and is therefore preferrable to burning liquidity, or sending liquidity NFT's to the dead address.
    uint256 public ETERNAL_LOCK = type(uint256).max;

    // a mapping of lock_id => Lock
    mapping(uint256 => Lock) public LOCKS;

    mapping(address => EnumerableSet.UintSet) USER_LOCKS; // a set of all lock_ids owned by a user, useful for on chain enumeration.

    constructor(
        ICountryList _countryList,
        address payable _autoCollectAddress,
        address payable _lpFeeReceiver,
        address payable _collectFeeReceiver
    ) {
        COUNTRY_LIST = _countryList;
        AUTO_COLLECT_ACCOUNT = _autoCollectAddress;
        FEE_ADDR_LP = _lpFeeReceiver;
        FEE_ADDR_COLLECT = _collectFeeReceiver;
        addOrEditFee("DEFAULT", 50, 200, 0, address(0));
        addOrEditFee("LVP", 80, 100, 0, address(0));
        addOrEditFee("LLP", 30, 350, 0, address(0));
    }

    function setFeeResolver(IFeeResolver _resolver) external onlyOwner {
        FEE_RESOLVER = _resolver;
    }

    function setFeeParams(
        address _autoCollectAccount,
        address payable _lpFeeReceiver,
        address payable _collectFeeReceiver
    ) external onlyOwner {
        AUTO_COLLECT_ACCOUNT = _autoCollectAccount;
        FEE_ADDR_LP = _lpFeeReceiver;
        FEE_ADDR_COLLECT = _collectFeeReceiver;
    }

    function addOrEditFee(
        string memory _name,
        uint256 _lpFee,
        uint256 _collectFee,
        uint256 _flatFee,
        address _flatFeeToken
    ) public onlyOwner {
        bytes32 nameHash = keccak256(abi.encodePacked(_name));

        FeeStruct memory newFee = FeeStruct(_name, _lpFee, _collectFee, _flatFee, _flatFeeToken);
        FEES[nameHash] = newFee;

        if (!FEE_LOOKUP.contains(nameHash)) {
            FEE_LOOKUP.add(nameHash);
            emit onAddFee(nameHash, newFee.name, newFee.lpFee, newFee.collectFee, newFee.flatFee, newFee.flatFeeToken);
        } else {
            emit onEditFee(nameHash, newFee.name, newFee.lpFee, newFee.collectFee, newFee.flatFee, newFee.flatFeeToken);
        }
    }

    function removeFee(string memory _name) external onlyOwner {
        bytes32 nameHash = keccak256(abi.encodePacked(_name));
        require(nameHash != keccak256(abi.encodePacked("DEFAULT")), "DEFAULT");
        require(FEE_LOOKUP.contains(nameHash));
        FEE_LOOKUP.remove(nameHash);
        emit onRemoveFee(nameHash);
    }

    function getFee(string memory _name) public view override returns (FeeStruct memory) {
        bytes32 feeHash = keccak256(abi.encodePacked(_name));
        require(FEE_LOOKUP.contains(feeHash), "NOT FOUND");
        return FEES[feeHash];
    }

    function getFeeOptionAtIndex(uint256 _index) external view returns (FeeStruct memory) {
        return FEES[FEE_LOOKUP.at(_index)];
    }

    function getFeeOptionLength() external view returns (uint256) {
        return FEE_LOOKUP.length();
    }

    function deductFlatFee(FeeStruct memory fee) private {
        if (fee.flatFeeToken == address(0)) {
            // fee in gas token
            require(msg.value == fee.flatFee, "FLAT FEE");
            FEE_ADDR_LP.transfer(fee.flatFee);
        } else {
            // fee in another token
            TransferHelper.safeTransferFrom(fee.flatFeeToken, msg.sender, FEE_ADDR_LP, fee.flatFee);
        }
    }

    /**
     * @dev converts nft to full range and collects fees and sends them back to collector
     * @param params The locking params as seen in IUNCX_ProofOfReservesV3.sol
     *
     * This function will fail if a liquidity position is out of range (100% token0, 0% token1) as it will not be able to create a full range position with counter liquidity.
     * This will also fail with rebasing tokens (liquidity nfts already stuck on univ3).
     */
    function lock(LockParams calldata params) external payable override nonReentrant returns (uint256) {
        require(params.owner != address(0));
        require(params.collectAddress != address(0), "COLLECT_ADDR");
        require(params.unlockDate < 1e10 || params.unlockDate == ETERNAL_LOCK, "MILLISECONDS"); // prevents errors when timestamp entered in milliseconds
        require(params.unlockDate > block.timestamp, "DATE PASSED");
        require(COUNTRY_LIST.countryIsValid(params.countryCode), "COUNTRY");
        FeeStruct memory fee;

        if (msg.sender == MIGRATE_IN) {
            fee.collectFee = abi.decode(params.r[0], (uint256));
        } else {
            if (params.r.length > 0) {
                fee = FEE_RESOLVER.useFee(params.r, msg.sender);
            } else {
                fee = getFee(params.feeName);
            }

            if (fee.flatFee > 0) {
                deductFlatFee(fee);
            }
        }

        params.nftPositionManager.safeTransferFrom(msg.sender, address(this), params.nft_id);

        Position memory position;
        (
            ,
            ,
            position.token0,
            position.token1,
            position.fee,
            position.tickLower,
            position.tickUpper,
            position.liquidity,
            ,
            ,
            ,
        ) = params.nftPositionManager.positions(params.nft_id);
        IUniswapV3Factory factory = IUniswapV3Factory(params.nftPositionManager.factory());
        address pool = factory.getPool(position.token0, position.token1, position.fee);
        int24 maxTick = tickSpacingToMaxTick(factory.feeAmountTickSpacing(position.fee));

        uint256 nftId;
        if (position.tickLower != -maxTick && position.tickUpper != maxTick) {
            // convert the position to full range by minting a new full range NFT
            nftId = _convertPositionToFullRange(
                params.nftPositionManager, params.nft_id, position, maxTick, params.dustRecipient
            );
        } else {
            nftId = params.nft_id;
            // collect fees for user to prevent being charged a fee on existing fees
            params.nftPositionManager.collect(
                INonfungiblePositionManager.CollectParams(
                    nftId, params.dustRecipient, type(uint128).max, type(uint128).max
                )
            );
        }

        // Take lp fee
        if (fee.lpFee > 0) {
            uint128 liquidity = _getLiquidity(params.nftPositionManager, nftId);
            params.nftPositionManager.decreaseLiquidity(
                INonfungiblePositionManager.DecreaseLiquidityParams(
                    nftId, uint128(liquidity * fee.lpFee / FEE_DENOMINATOR), 0, 0, block.timestamp
                )
            );
            params.nftPositionManager.collect(
                INonfungiblePositionManager.CollectParams(nftId, FEE_ADDR_LP, type(uint128).max, type(uint128).max)
            );
        }

        Lock memory newLock;
        newLock.lock_id = NONCE;
        newLock.nftPositionManager = params.nftPositionManager;
        newLock.pool = pool;
        newLock.nft_id = nftId;
        newLock.owner = params.owner;
        newLock.additionalCollector = params.additionalCollector;
        newLock.collectAddress = params.collectAddress;
        newLock.unlockDate = params.unlockDate;
        newLock.countryCode = params.countryCode;
        newLock.ucf = fee.collectFee;
        LOCKS[NONCE] = newLock;
        USER_LOCKS[params.owner].add(NONCE);
        NONCE++;

        emitLockEvent(newLock.lock_id);

        return newLock.lock_id;
    }

    function emitLockEvent(uint256 _lockId) private {
        Lock memory newLock = LOCKS[_lockId];
        Position memory position;
        (
            ,
            ,
            position.token0,
            position.token1,
            position.fee,
            position.tickLower,
            position.tickUpper,
            position.liquidity,
            ,
            ,
            ,
        ) = newLock.nftPositionManager.positions(newLock.nft_id);
        emit onLock(
            newLock.lock_id,
            address(newLock.nftPositionManager),
            newLock.nft_id,
            newLock.owner,
            newLock.additionalCollector,
            newLock.collectAddress,
            newLock.unlockDate,
            newLock.countryCode,
            newLock.ucf,
            newLock.pool,
            position
        );
    }

    function _convertPositionToFullRange(
        INonfungiblePositionManager _nftPositionManager,
        uint256 _tokenId,
        Position memory _position,
        int24 _maxTick,
        address _dustRecipient
    ) private returns (uint256) {
        _nftPositionManager.decreaseLiquidity(
            INonfungiblePositionManager.DecreaseLiquidityParams(_tokenId, _position.liquidity, 0, 0, block.timestamp)
        );
        (uint256 collectedAmount0, uint256 collectedAmount1) = _nftPositionManager.collect(
            INonfungiblePositionManager.CollectParams(_tokenId, address(this), type(uint128).max, type(uint128).max)
        );

        INonfungiblePositionManager.MintParams memory mintParams =
            _setPartialMintParamsFromPosition(_nftPositionManager, _tokenId);

        mintParams.deadline = block.timestamp;
        mintParams.recipient = address(this);
        mintParams.tickLower = -_maxTick;
        mintParams.tickUpper = _maxTick;
        mintParams.amount0Desired = collectedAmount0;
        mintParams.amount1Desired = collectedAmount1;
        mintParams.amount0Min = 0;
        mintParams.amount1Min = 0;

        TransferHelper.safeApprove(mintParams.token0, address(_nftPositionManager), mintParams.amount0Desired);
        TransferHelper.safeApprove(mintParams.token1, address(_nftPositionManager), mintParams.amount1Desired);

        (uint256 newNftId,, uint256 mintedAmount0, uint256 mintedAmount1) = _nftPositionManager.mint(mintParams);

        _nftPositionManager.burn(_tokenId);

        // Refund the tokens which dont fit into full range liquidity
        if (collectedAmount0 > mintedAmount0) {
            TransferHelper.safeTransfer(mintParams.token0, _dustRecipient, collectedAmount0 - mintedAmount0);
        }
        if (collectedAmount1 > mintedAmount1) {
            TransferHelper.safeTransfer(mintParams.token1, _dustRecipient, collectedAmount1 - mintedAmount1);
        }
        return newNftId;
    }

    /**
     * @dev Collect fees to _recipient if msg.sender is the owner of _lockId
     */
    function collect(uint256 _lockId, address _recipient, uint128 _amount0Max, uint128 _amount1Max)
        external
        override
        nonReentrant
        returns (uint256 amount0, uint256 amount1, uint256 fee0, uint256 fee1)
    {
        (amount0, amount1, fee0, fee1) = _collect(_lockId, _recipient, _amount0Max, _amount1Max);
    }

    /**
     * @dev Private collect function, wrap this in re-entrancy guard calls
     */
    function _collect(uint256 _lockId, address _recipient, uint128 _amount0Max, uint128 _amount1Max)
        private
        returns (uint256 amount0, uint256 amount1, uint256 fee0, uint256 fee1)
    {
        Lock memory userLock = LOCKS[_lockId];
        bool collectorIsBot = AUTO_COLLECT_ACCOUNT == msg.sender;
        require(userLock.owner == msg.sender || userLock.additionalCollector == msg.sender || collectorIsBot, "OWNER");
        if (userLock.ucf == 0) {
            // No Protocol fee
            (amount0, amount1) = userLock.nftPositionManager.collect(
                INonfungiblePositionManager.CollectParams(userLock.nft_id, _recipient, _amount0Max, _amount1Max)
            );
        } else {
            // Protocol fees
            (,, address _token0, address _token1,,,,,,,,) = userLock.nftPositionManager.positions(userLock.nft_id);
            (uint256 balance0, uint256 balance1) = userLock.nftPositionManager.collect(
                INonfungiblePositionManager.CollectParams(userLock.nft_id, address(this), _amount0Max, _amount1Max)
            );

            address feeTo = collectorIsBot ? _recipient : FEE_ADDR_COLLECT;
            address remainderTo = collectorIsBot ? userLock.collectAddress : _recipient;

            if (balance0 > 0) {
                fee0 = balance0 * userLock.ucf / FEE_DENOMINATOR;
                TransferHelper.safeTransfer(_token0, feeTo, fee0);
                amount0 = balance0 - fee0;
                TransferHelper.safeTransfer(_token0, remainderTo, amount0);
            }
            if (balance1 > 0) {
                fee1 = balance1 * userLock.ucf / FEE_DENOMINATOR;
                TransferHelper.safeTransfer(_token1, feeTo, fee1);
                amount1 = balance1 - fee1;
                TransferHelper.safeTransfer(_token1, remainderTo, amount1);
            }
        }
    }

    /**
     * @dev increases liquidity. Can be called by anyone.
     * You should ideally call increaseLiquidity from the NftPositionManager directly for gas efficiency.
     * This method is here just for convenience for some contracts which solely interact with the UNCX lockers / lockIds
     */
    function increaseLiquidity(uint256 _lockId, INonfungiblePositionManager.IncreaseLiquidityParams calldata params)
        external
        payable
        override
        nonReentrant
        returns (uint128 liquidity, uint256 amount0, uint256 amount1)
    {
        Lock memory userLock = LOCKS[_lockId];
        require(userLock.nft_id == params.tokenId, "NFT ID");

        (,, address token0, address token1,,,,,,,,) = userLock.nftPositionManager.positions(userLock.nft_id);
        TransferHelper.safeTransferFrom(token0, msg.sender, address(this), params.amount0Desired);
        TransferHelper.safeTransferFrom(token1, msg.sender, address(this), params.amount1Desired);
        TransferHelper.safeApprove(token0, address(userLock.nftPositionManager), params.amount0Desired);
        TransferHelper.safeApprove(token1, address(userLock.nftPositionManager), params.amount1Desired);

        (liquidity, amount0, amount1) = userLock.nftPositionManager.increaseLiquidity(params);
        emit onIncreaseLiquidity(_lockId); // This can be called directly from the NFT position manager in which case this event won't fire
    }

    /**
     * @dev decrease liquidity if a lock has expired (useful before relocking)
     */
    function decreaseLiquidity(uint256 _lockId, INonfungiblePositionManager.DecreaseLiquidityParams calldata params)
        external
        payable
        override
        nonReentrant
        returns (uint256 amount0, uint256 amount1)
    {
        isLockAdmin(_lockId);
        Lock memory userLock = LOCKS[_lockId];
        require(userLock.nft_id == params.tokenId, "NFT ID");
        if (userLock.unlockDate == ETERNAL_LOCK) {
            revert("ETERNAL_LOCK");
        } else {
            require(userLock.unlockDate < block.timestamp, "NOT YET");
        }
        (amount0, amount1) = userLock.nftPositionManager.decreaseLiquidity(params);
        userLock.nftPositionManager.collect(
            INonfungiblePositionManager.CollectParams(userLock.nft_id, msg.sender, type(uint128).max, type(uint128).max)
        );
        emit onDecreaseLiquidity(_lockId);
    }

    /**
     * @dev set the unlock date further in the future
     */
    function relock(uint256 _lockId, uint256 _unlockDate) external override nonReentrant {
        isLockAdmin(_lockId);
        Lock storage userLock = LOCKS[_lockId];
        require(_unlockDate > userLock.unlockDate, "DATE");
        require(_unlockDate > block.timestamp, "DATE PASSED");
        require(_unlockDate < 1e10 || _unlockDate == ETERNAL_LOCK, "MILLISECONDS"); // prevents errors when timestamp entered in milliseconds
        userLock.unlockDate = _unlockDate;
        emit onRelock(_lockId, userLock.unlockDate);
    }

    /**
     * @dev withdraw a UniV3 liquidity NFT and send it to _receiver
     * Only callable once unlockDate has expired
     */
    function withdraw(uint256 _lockId, address _receiver) external override nonReentrant {
        isLockAdmin(_lockId);
        Lock memory userLock = LOCKS[_lockId];
        if (userLock.unlockDate == ETERNAL_LOCK) {
            revert("ETERNAL_LOCK");
        } else {
            require(userLock.unlockDate < block.timestamp, "NOT YET");
        }

        if (userLock.ucf > 0) {
            _collect(_lockId, _receiver, type(uint128).max, type(uint128).max);
        }

        userLock.nftPositionManager.safeTransferFrom(address(this), _receiver, userLock.nft_id);
        USER_LOCKS[userLock.owner].remove(_lockId);

        emit onWithdraw(_lockId, userLock.owner, _receiver);

        delete LOCKS[_lockId]; // clear the state for this lock (reset all values to zero)
    }

    /**
     * @dev set migrate in contract address
     */
    function setMigrateInContract(address _migrateIn) external override onlyOwner {
        MIGRATE_IN = _migrateIn;
    }

    /**
     * @dev migrate a lock to a new amm version (Uniswap V4)
     */
    function migrate(uint256 _lockId) external override nonReentrant {
        require(address(MIGRATOR) != address(0), "NOT SET");
        isLockAdmin(_lockId);
        Lock memory userLock = LOCKS[_lockId];
        userLock.nftPositionManager.approve(address(MIGRATOR), userLock.nft_id);
        MIGRATOR.migrate(_lockId, userLock.nftPositionManager, userLock.nft_id);
        USER_LOCKS[userLock.owner].remove(_lockId);

        delete LOCKS[_lockId]; // clear the state for this lock (reset all values to zero)

        emit onMigrate(_lockId);
    }

    /**
     * @dev allow a lock owner to add an additional address, usually a contract, to collect fees. Useful for bots
     */
    function setAdditionalCollector(uint256 _lockId, address _additionalCollector) external override nonReentrant {
        isLockAdmin(_lockId);
        Lock storage userLock = LOCKS[_lockId];
        userLock.additionalCollector = _additionalCollector;

        emit onSetAdditionalCollector(_lockId, _additionalCollector);
    }

    /**
     * @dev set the adress to which fees are automatically collected
     */
    function setCollectAddress(uint256 _lockId, address _collectAddress) external override nonReentrant {
        isLockAdmin(_lockId);
        require(_collectAddress != address(0), "COLLECT_ADDR");
        Lock storage userLock = LOCKS[_lockId];
        userLock.collectAddress = _collectAddress;

        emit onSetCollectAddress(_lockId, _collectAddress);
    }

    /**
     * @dev transfer ownership of a lock to _newOwner
     */
    function transferLockOwnership(uint256 _lockId, address _newOwner) external override nonReentrant {
        isLockAdmin(_lockId);
        require(msg.sender != _newOwner, "SAME OWNER");
        Lock storage userLock = LOCKS[_lockId];
        userLock.pendingOwner = _newOwner;

        emit onLockOwnershipTransferStarted(_lockId, msg.sender, _newOwner);
    }

    /**
     * @dev accept lock ownership transfer
     */
    function acceptLockOwnership(uint256 _lockId) external override nonReentrant {
        Lock storage userLock = LOCKS[_lockId];
        require(userLock.pendingOwner == msg.sender, "OWNER");

        address oldOwner = userLock.owner;
        USER_LOCKS[userLock.owner].remove(_lockId);
        userLock.owner = msg.sender;
        userLock.pendingOwner = address(0);
        USER_LOCKS[msg.sender].add(_lockId);

        emit onTransferLockOwnership(_lockId, oldOwner, msg.sender);
    }

    /**
     * @dev set the migrator contract which allows locked LP NFT's to be migrated to future AMM versions
     */
    function setMigrator(address _migrator) external override onlyOwner {
        MIGRATOR = IMigrateV3NFT(_migrator);

        emit onSetMigrator(_migrator);
    }

    /**
     * @dev set ucf
     */
    function setUCF(uint256 _lockId, uint256 _ucf) external override onlyOwner {
        Lock storage l = LOCKS[_lockId];
        require(_ucf < l.ucf, "L");
        l.ucf = _ucf;
        emit onSetUCF(_lockId, _ucf);
    }

    /**
     * @dev check if msg.sender is the owner of lock with _lockId
     */
    function isLockAdmin(uint256 _lockId) private view {
        Lock memory userLock = LOCKS[_lockId];
        require(userLock.owner == msg.sender, "OWNER");
    }

    /**
     * @dev returns a Lock struct for _lockId
     */
    function getLock(uint256 _lockId) external view override returns (Lock memory _lock) {
        _lock = LOCKS[_lockId];
    }

    /**
     * @dev gets the number of unique locks in this contract, used to page through the lock array (includes expired and withdrawn locks)
     */
    function getLocksLength() external view override returns (uint256) {
        return NONCE;
    }

    /**
     * @dev gets the number of locks for a user
     */
    function getNumUserLocks(address _user) external view override returns (uint256) {
        return USER_LOCKS[_user].length();
    }

    /**
     * @dev gets the lock at a specific index for a user
     */
    function getUserLockAtIndex(address _user, uint256 _index) external view override returns (Lock memory) {
        return LOCKS[USER_LOCKS[_user].at(_index)];
    }

    /**
     * @dev gets the maximum tick for a tickSpacing
     * source: https://github.com/Uniswap/v3-core/blob/main/contracts/libraries/Tick.sol
     */
    function tickSpacingToMaxTick(int24 tickSpacing) public pure returns (int24 maxTick) {
        maxTick = (887272 / tickSpacing) * tickSpacing;
    }

    function _setPartialMintParamsFromPosition(INonfungiblePositionManager _nftPositionManager, uint256 _tokenId)
        private
        view
        returns (INonfungiblePositionManager.MintParams memory)
    {
        INonfungiblePositionManager.MintParams memory m;
        (,, m.token0, m.token1, m.fee,,,,,,,) = _nftPositionManager.positions(_tokenId);
        return m;
    }

    /**
     * @dev get a locks liquidity in amounts of token0 and token1 for a generic position (not from state)
     */
    function getAmountsForLiquidity(int24 currentTick, int24 tickLower, int24 tickHigher, uint128 liquidity)
        public
        pure
        override
        returns (uint256 amount0, uint256 amount1)
    {
        return LiquidityAmounts.getAmountsForLiquidity(
            TickMath.getSqrtRatioAtTick(currentTick),
            TickMath.getSqrtRatioAtTick(tickLower),
            TickMath.getSqrtRatioAtTick(tickHigher),
            liquidity
        );
    }

    /**
     * @dev returns just the liquidity value from a position
     */
    function _getLiquidity(INonfungiblePositionManager _nftPositionManager, uint256 _tokenId)
        private
        view
        returns (uint128)
    {
        (,,,,,,, uint128 liquidity,,,,) = _nftPositionManager.positions(_tokenId);
        return liquidity;
    }

    /**
     * @dev Allows admin to remove any eth mistakenly sent to the contract
     */
    function adminRefundEth(uint256 _amount, address payable _receiver) external onlyOwner nonReentrant {
        _receiver.transfer(_amount);
    }

    /**
     * @dev Allows admin to remove any ERC20's mistakenly sent to the contract
     * Since this contract is only for locking NFT liquidity, this allows removal of ERC20 tokens and cannot remove locked NFT liquidity.
     */
    function adminRefundERC20(address _token, address _receiver, uint256 _amount) external onlyOwner nonReentrant {
        // TransferHelper.safeTransfer = token.call(abi.encodeWithSelector(IERC20.transfer.selector, to, value));
        // Attempting to transfer nfts with this function (substituting a nft_id for _amount) wil fail with 'ST' as NFTS do not have the same interface
        TransferHelper.safeTransfer(_token, _receiver, _amount);
    }

    function onERC721Received(address operator, address from, uint256 tokenId, bytes calldata data)
        public
        pure
        override
        returns (bytes4)
    {
        return IERC721Receiver.onERC721Received.selector;
    }
}
