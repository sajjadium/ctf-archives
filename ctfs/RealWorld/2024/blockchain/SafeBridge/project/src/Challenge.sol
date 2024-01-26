pragma solidity ^0.8.20;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract Challenge {
    address public immutable BRIDGE;
    address public immutable MESSENGER;
    address public immutable WETH;

    constructor(address bridge, address messenger, address weth) {
        BRIDGE = bridge;
        MESSENGER = messenger;
        WETH = weth;
    }

    function isSolved() external view returns (bool) {
        return IERC20(WETH).balanceOf(BRIDGE) == 0;
    }
}
