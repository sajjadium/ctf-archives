pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract KAsinoChips is ERC20 {
    bool public buyinClosed = false;

    constructor(uint256 initialSupply) ERC20("KAsino chip", "KAC") {
        _mint(msg.sender, initialSupply);
    }

    function buyin() public payable {
        require(msg.value >= .1 ether, "This is a premium KAsino");
        require(!buyinClosed, "Buyins are already closed");

        buyinClosed = true;
        _mint(msg.sender, 100);
    }
}
