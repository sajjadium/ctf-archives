// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.16;

import "./MasterHelper.sol";

interface WETH9 is ERC20 {
    function deposit() external payable;
}

contract Setup {
    
    WETH9 public constant weth = WETH9(0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2);
    MasterHelper public immutable mHelper;

    constructor() payable {
        mHelper = new MasterHelper();
        weth.deposit{value: 10 ether}();
        weth.transfer(address(mHelper), 10 ether); 
    }

    function isSolved() external view returns (bool) {
        return weth.balanceOf(address(mHelper)) == 0;
    }

}