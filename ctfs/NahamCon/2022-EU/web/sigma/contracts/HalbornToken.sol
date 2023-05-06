// SPDX-License-Identifier: Unlicensed
// @author - Ataberk Yavuzer
pragma solidity ^0.8.0;

import { ERC20 } from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract HalbornToken is ERC20{
    constructor(address _escrowContract) ERC20("Halborn Token", "HAL") {
        require(_escrowContract != address(0), "HalbornToken::zero address");
        _mint(_escrowContract, 1 ether);
    }

    function transfer(address to, uint256 amount) public virtual override returns (bool){
        (to, amount);
        revert("HalbornToken::transfer() method is not allowed");
    }
}