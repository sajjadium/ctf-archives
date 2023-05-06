pragma solidity ^0.8.13;

import "./Chal.sol";

contract Setup {
    Chal public immutable TARGET;

    address private constant UNISWAP_V2_ROUTER = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;
    address private constant WETH = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    address private constant DAI = 0x6B175474E89094C44Da98b954EedeAC495271d0F;
    address private constant USDC = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;

    IUniswapV2Router private router = IUniswapV2Router(UNISWAP_V2_ROUTER);
    IERC20 private dai = IERC20(DAI);
    IERC20 private usdc = IERC20(USDC);
    IWETH9 private weth = IWETH9(WETH);

    uint private initialBalance;

    constructor() payable {
        TARGET = new Chal();

        require(msg.value == 100 ether);

        weth.deposit{ value: 100 ether }();

        weth.approve(address(router), type(uint256).max);
        dai.approve(address(router), type(uint256).max);
        usdc.approve(address(router), type(uint256).max);

        address[] memory path;
        path = new address[](2);

        {
            path[0] = WETH;
            path[1] = USDC;
            uint[] memory amounts = router.swapExactTokensForTokens(
                50 ether,
                0,
                path,
                address(TARGET),
                block.timestamp
            );
        }

        {
            path[0] = WETH;
            path[1] = DAI;
            uint[] memory amounts = router.swapExactTokensForTokens(
                50 ether,
                0,
                path,
                address(TARGET),
                block.timestamp
            );
        }

        initialBalance = curTargetBalance();
    }

    function curTargetBalance() public view returns (uint) {
        return usdc.balanceOf(address(TARGET)) + dai.balanceOf(address(TARGET))/10e12;
    }

    function isSolved() public view returns (bool) {
        return curTargetBalance() < (initialBalance / 10);
    }
}