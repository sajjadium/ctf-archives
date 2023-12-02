// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract WannaETH is ERC20 {
    constructor() ERC20("WannaETH", "WETH") {
        _mint(msg.sender, 1_000_000 * 10 ** 18);
    }

    receive() external payable {
        deposit();
    }

    fallback() external payable {
        deposit();
    }

    function deposit() public payable {
        _mint(msg.sender, msg.value);
    }

    function withdraw(uint256 amount) public {
        require(balanceOf(msg.sender) >= amount);
        _burn(msg.sender, amount);
    }
}
