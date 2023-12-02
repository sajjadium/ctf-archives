// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;

import "./WannaETH.sol";
import "./PhantomToken.sol";
import "./Vault.sol";

contract Setup {
    WannaETH public immutable weth;
    PhantomToken public immutable pmt;

    Vault public immutable vault;

    constructor() {
        weth = new WannaETH();
        pmt = new PhantomToken();
        vault = new Vault(payable(address(weth)), payable(address(pmt)));

        weth.approve(address(vault), type(uint256).max);
        pmt.approve(address(vault), type(uint256).max);

        vault.deposit(address(weth), 1);
        vault.deposit(address(pmt), 1);
    }

    function isSolved() external view returns (bool) {
        return (vault.totalDeposited() > 1_000 * 10 ** 18);
    }
}
