// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "./Factory.sol";
import "./NFT.sol";
import "./Randomness.sol";
import "./ItemShop.sol";

contract Challenge {
    Factory public immutable FACTORY;
    ItemShop public immutable ITEMSHOP;
    NFT public immutable TOKEN;

    constructor(Factory factory, ItemShop itemShop, NFT token) {
        FACTORY = factory;
        ITEMSHOP = itemShop;
        TOKEN = token;
    }

    function isSolved() public view returns (bool) {
        return TOKEN.balanceOf(address(TOKEN)) == 0;
    }
}
