// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "../lib/openzeppelin-contracts/contracts/token/ERC721/IERC721.sol";
import "./Split.sol";

contract Challenge {
    Split public immutable SPLIT;

    constructor(Split split) {
        SPLIT = split;
    }

    function isSolved() external view returns (bool) {
        Split.SplitData memory splitData = SPLIT.splitsById(0);

        return address(SPLIT).balance == 0 && address(splitData.wallet).balance == 0;
    }
}
