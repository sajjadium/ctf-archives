// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8;

import "@openzeppelin-upgradeable/token/ERC1155/IERC1155Upgradeable.sol";
import "./Constants.sol";

interface INFT {
    event RequestOffchainRandomness();

    function initialize(bytes calldata initialization) external;
    function transferOwnership(address to) external;
    function resolveRandomness(bytes32 seed) external;
}

interface IFactory {
    function isItemShopApprovedByFactory(address itemShop) external view returns (bool);
    function randomnessOperator() external view returns (address);
}

interface IRandomness {
    function generate(bytes32 seed, uint256 rounds) external returns (bytes32);
}

interface IItemShop is IERC1155Upgradeable {
    function initialize(bytes calldata initialization) external;
    function buy(uint256 itemId) external payable;
    function burn(address account, uint256 id, uint256 value) external;
    function itemInfo(uint256 tokenId) external view returns (ItemInfo memory);
}

interface IFighter {
    function getInput(FighterVars calldata attacker, FighterVars calldata attackee) external returns (uint256 inputs);
}
