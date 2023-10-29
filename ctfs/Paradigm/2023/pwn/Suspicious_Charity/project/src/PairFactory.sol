// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "./Pair.sol";
import "./lib/PairName.sol";

contract PairFactory {
    using PairName for uint256;

    address private level;

    uint256 public tokenName;
    uint256 public tokenSymbol;

    mapping(address => mapping(address => address)) public getPair;
    mapping(address => bool) public isPairs;
    address[] public allPairs;

    modifier ensure(uint256 deadline) {
        require(deadline >= block.number, "EXPIRED");
        _;
    }

    constructor() {
        level = msg.sender;
        tokenName = 0x31;
        tokenSymbol = 0x31;
    }

    modifier onlyLevel() {
        require(msg.sender == level);
        _;
    }

    function createPair(address tokenA, address tokenB) external onlyLevel returns (address pair) {
        (address token0, address token1) = sortTokens(tokenA, tokenB);
        require(getPair[token0][token1] == address(0), "PAIR_EXISTS");

        pair = address(
            new Pair(
            token0,
            token1,
            string.concat("LP Token", tokenName.toString()),
            string.concat("LP", tokenSymbol.toString())
            )
        );

        tokenName = tokenName.nextId();
        tokenSymbol = tokenSymbol.nextId();

        isPairs[pair] = true;
        getPair[token0][token1] = pair;
        getPair[token1][token0] = pair;
        allPairs.push(pair);
    }

    function _addLiquidity(
        address tokenA,
        address tokenB,
        uint256 amountADesired,
        uint256 amountBDesired,
        uint256 amountAMin,
        uint256 amountBMin
    ) internal view returns (uint256 amountA, uint256 amountB) {
        (uint256 reserveA, uint256 reserveB) = getReserves(tokenA, tokenB);
        if (reserveA == 0 && reserveB == 0) {
            (amountA, amountB) = (amountADesired, amountBDesired);
        } else {
            uint256 amountBOptimal = quote(amountADesired, reserveA, reserveB);
            if (amountBOptimal <= amountBDesired) {
                require(amountBOptimal >= amountBMin, "INSUFFICIENT_B_AMOUNT");
                (amountA, amountB) = (amountADesired, amountBOptimal);
            } else {
                uint256 amountAOptimal = quote(amountBDesired, reserveB, reserveA);
                assert(amountAOptimal <= amountADesired);
                require(amountAOptimal >= amountAMin, "INSUFFICIENT_A_AMOUNT");
                (amountA, amountB) = (amountAOptimal, amountBDesired);
            }
        }
    }

    function addLiquidity(
        address tokenA,
        address tokenB,
        uint256 amountADesired,
        uint256 amountBDesired,
        uint256 amountAMin,
        uint256 amountBMin,
        address to,
        uint256 deadline
    ) external ensure(deadline) returns (uint256 amountA, uint256 amountB, uint256 liquidity) {
        (amountA, amountB) = _addLiquidity(tokenA, tokenB, amountADesired, amountBDesired, amountAMin, amountBMin);
        address pair = getPair[tokenA][tokenB];

        require(IERC20(tokenA).transferFrom(msg.sender, pair, amountA), "FAIL_TRANSFER");
        require(IERC20(tokenB).transferFrom(msg.sender, pair, amountB), "FAIL_TRANSFER");

        liquidity = Pair(pair).mint(to);
    }

    function removeLiquidity(
        address tokenA,
        address tokenB,
        uint256 liquidity,
        uint256 amountAMin,
        uint256 amountBMin,
        address to,
        uint256 deadline
    ) external ensure(deadline) returns (uint256 amountA, uint256 amountB) {
        address pair = getPair[tokenA][tokenB];
        require(Pair(pair).transferFrom(msg.sender, pair, liquidity), "FAIL_TRANSFER");
        (uint256 amount0, uint256 amount1) = Pair(pair).burn(to);
        (address token0,) = sortTokens(tokenA, tokenB);
        (amountA, amountB) = tokenA == token0 ? (amount0, amount1) : (amount1, amount0);
        require(amountA >= amountAMin, "INSUFFICIENT_A_AMOUNT");
        require(amountB >= amountBMin, "INSUFFICIENT_B_AMOUNT");
    }

    function getReserves(address tokenA, address tokenB) internal view returns (uint256 reserveA, uint256 reserveB) {
        (address token0,) = sortTokens(tokenA, tokenB);
        (uint256 reserve0, uint256 reserve1) = Pair(getPair[tokenA][tokenB]).getReserves();
        (reserveA, reserveB) = tokenA == token0 ? (reserve0, reserve1) : (reserve1, reserve0);
    }

    function quote(uint256 amountA, uint256 reserveA, uint256 reserveB) internal pure returns (uint256 amountB) {
        require(amountA > 0, "INSUFFICIENT_AMOUNT");
        require(reserveA > 0 && reserveB > 0, "INSUFFICIENT_LIQUIDITY");
        amountB = amountA * reserveB / reserveA;
    }

    function sortTokens(address tokenA, address tokenB) internal pure returns (address token0, address token1) {
        require(tokenA != tokenB, "IDENTICAL_ADDRESSES");
        (token0, token1) = tokenA < tokenB ? (tokenA, tokenB) : (tokenB, tokenA);
        require(token0 != address(0), "ZERO_ADDRESS");
    }
}
