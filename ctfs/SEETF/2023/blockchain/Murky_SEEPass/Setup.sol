// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;

import "./SEEPass.sol";

contract Setup {
    SEEPass public immutable pass;

    constructor(bytes32 _merkleRoot) {
        pass = new SEEPass(_merkleRoot);
    }

    function isSolved() external view returns (bool) {
        return pass.balanceOf(msg.sender) > 0;
    }
}
