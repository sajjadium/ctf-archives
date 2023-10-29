// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract InuToken is ERC20 {
    constructor() ERC20("Inu Token", "INU") {
        _mint(msg.sender, 1_000_000_000 ether);
    }
}
