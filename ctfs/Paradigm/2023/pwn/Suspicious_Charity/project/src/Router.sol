// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "./TokenFactory.sol";
import "./PairFactory.sol";
import "./FlagCharity.sol";

contract Router {
    uint256 constant BUDGET_CAP = 100 ether;
    uint256 constant LISTING_CAP = 200;

    TokenFactory public tokenFactory;
    PairFactory public pairFactory;
    FlagCharity public flagCharity;

    uint256 public totalMint;
    uint256 public totalListing;

    mapping(address => uint256) public priceOf;
    address[] public listingTokens;
    address[] public lpTokens;

    modifier onlyAllowListToken(address token) {
        require(tokenFactory.tokens(token), "ONLY_ALLOWLIST_TOKEN");
        _;
    }

    modifier onlyListedToken(address token) {
        require(priceOf[token] != 0, "ONLY_LISTED_TOKEN");
        _;
    }

    constructor() {
        tokenFactory = new TokenFactory();
        pairFactory = new PairFactory();
        flagCharity = new FlagCharity();
    }

    function donate(address token, uint256 amount) external {
        require(priceOf[token] != 0 || pairFactory.isPairs(token), "CHECK_TOKEN");
        require(amount > 0, "ZERO_AMOUNT");
        require(IERC20(token).transferFrom(msg.sender, address(this), amount), "FAIL_TRANSFER");

        IERC20(token).approve(address(flagCharity), amount);
        flagCharity.donate(msg.sender, token, amount);
    }

    function createToken(string memory token_name, string memory token_symbol) external returns (address) {
        return tokenFactory.createToken(token_name, token_symbol);
    }

    function createPair(address tokenA, address tokenB) external returns (address pair) {
        require(tokenFactory.tokens(tokenA) && tokenFactory.tokens(tokenB), "ONLY_ALLOWLIST_TOKEN");

        pair = pairFactory.createPair(tokenA, tokenB);
        lpTokens.push(pair);
    }

    function listing(address token, uint256 price) external onlyAllowListToken(token) {
        require(totalListing <= LISTING_CAP, "EXCEED_LISTING_CAP");
        require(price != 0, "ZERO_PRICE");
        require(priceOf[token] == 0, "ALREADY_LISTED");

        priceOf[token] = price;
        totalListing += 1;

        listingTokens.push(token);
    }

    function mint(address token, uint256 amount) external onlyListedToken(token) {
        require(amount * priceOf[token] + totalMint <= BUDGET_CAP, "EXCEED_BUDGET_CAP");

        tokenFactory.tokenMint(token, msg.sender, amount);
        totalMint += amount * priceOf[token];
    }

    // Helper functions
    function listingTokensCount() external view returns (uint256) {
        return listingTokens.length;
    }

    function lpTokensCount() external view returns (uint256) {
        return lpTokens.length;
    }

    function lpTokensInfo(uint256 i) external view returns (string memory, address) {
        address lpToken = lpTokens[i];
        Pair pair = Pair(lpToken);
        return (pair.name(), lpToken);
    }

    function lpTokensStatus(address pair_address) external view returns (uint256, uint256, uint256) {
        Pair pair = Pair(pair_address);
        (uint256 reserve0, uint256 reserve1) = pair.getReserves();
        uint256 totalSupply = pair.totalSupply();
        return (reserve0, reserve1, totalSupply);
    }

    function lpTokenPair(uint256 i) external view returns (address, address) {
        Pair pair = Pair(lpTokens[i]);
        return (pair.token0(), pair.token1());
    }
}
