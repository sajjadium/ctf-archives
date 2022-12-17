// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract SimpleToken is ERC20 {

    address public airdropAddress;
    address owner;

    constructor(
        string memory name,
        string memory symbol
    ) ERC20(name, symbol) {
        owner = msg.sender;
    }

    modifier checkZeroAddress(address _address) {
        require(_address != address(0), "Address cannot be zero");
        _;
    }

    modifier onlyOwner() {
        require(msg.sender == owner,"Not authorized");
        _;
    }

    function setAirdropAddress(address newAddr) 
        external 
        checkZeroAddress(newAddr) 
        onlyOwner
    {
        airdropAddress = newAddr;
    }

    function mint(address addr, uint256 amount) external{
        require(msg.sender == airdropAddress, "You can't call this");
        _mint(addr, amount);
    }
}