// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract WETH is ERC20 {
    event Deposit(address indexed dst, uint256 wad);
    event Withdrawal(address indexed src, uint256 wad);

    constructor() ERC20("Wrapped Ether", "WETH") {}

    receive() external payable {
        deposit();
    }

    function deposit() public payable {
        address sender = _msgSender();

        _mint(sender, msg.value);

        emit Deposit(sender, msg.value);
    }

    function withdraw(uint256 wad) external {
        address sender = _msgSender();

        _burn(sender, wad);

        (bool success,) = sender.call{value: wad}("");
        require(success, "withdraw ETH failed");

        emit Withdrawal(sender, wad);
    }
}
