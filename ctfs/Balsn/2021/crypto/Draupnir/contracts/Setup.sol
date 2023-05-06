// SPDX-License-Identifier: GPL-3.0-or-later

pragma solidity 0.8.9;

import "./weth9.sol";

contract Setup {
    WETH9 public weth;

    constructor() payable {
        require(msg.value == 100 ether);
        weth = new WETH9();
        weth.deposit{value:msg.value}();
        return;
    }

    function isSolved() external view returns (bool) {
        return address(weth).balance == 0;
    }
}
