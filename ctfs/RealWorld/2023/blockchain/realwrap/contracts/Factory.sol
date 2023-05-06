pragma solidity ^0.8.17;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "./UniswapV2Pair.sol";

contract SimpleToken is ERC20 {
    constructor(uint256 _initialSupply) ERC20("SimpleToken", "SPT") {
        _mint(msg.sender, _initialSupply);
    }
}

interface IUniswapV2Pair {
    function getReserves()
        external
        view
        returns (uint112 reserve0, uint112 reserve1, uint32 blockTimestampLast);

    function mint(address to) external returns (uint liquidity);

    function initialize(address, address) external;
}

contract Factory {
    address public constant WETH = 0x0000000000000000000000000000000000004eA1;
    address public uniswapV2Pair;

    event PairCreated(
        address indexed token0,
        address indexed token1,
        address pair
    );

    constructor() payable {
        require(msg.value == 1 ether);
        address token = address(new SimpleToken(10 ** 8 * 1 ether));
        uniswapV2Pair = createPair(WETH, token);
        IERC20(WETH).transfer(uniswapV2Pair, 1 ether);
        IERC20(token).transfer(uniswapV2Pair, 100 ether);
        IUniswapV2Pair(uniswapV2Pair).mint(msg.sender);
    }

    function createPair(
        address tokenA,
        address tokenB
    ) public returns (address pair) {
        (address token0, address token1) = tokenA < tokenB
            ? (tokenA, tokenB)
            : (tokenB, tokenA);
        bytes32 salt = keccak256(abi.encodePacked(token0, token1));
        pair = address(new UniswapV2Pair{salt: salt}());
        IUniswapV2Pair(pair).initialize(token0, token1);
        emit PairCreated(token0, token1, pair);
    }

    function isSolved() public view returns (bool) {
        (uint256 reserve0, uint256 reserve1, ) = IUniswapV2Pair(uniswapV2Pair)
            .getReserves();
        return reserve0 == 0 && reserve1 == 0;
    }
}
