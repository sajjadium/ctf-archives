// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@uniswap/merkle-distributor/contracts/interfaces/IMerkleDistributor.sol";

contract Challenge {
    IMerkleDistributor public immutable MERKLE_DISTRIBUTOR;

    constructor(IMerkleDistributor distributor) {
        MERKLE_DISTRIBUTOR = distributor;
    }

    function getScore() external view returns (uint256) {
        return IERC20(MERKLE_DISTRIBUTOR.token()).balanceOf(address(this)) / 1 ether;
    }
}
