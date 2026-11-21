// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

contract GlacierCoin
{
    address owner;
    mapping(address => uint) public balances;
    mapping(address => uint) public frozen;

    constructor() 
    {
        owner = msg.sender;
    }

    //This is the function you need to call to buy tokens
    function buy() public payable
    {
        _mint(msg.value, msg.sender);
    }

    //This is the function you need to call to burn tokens
    function burn(uint256 amount) public
    {
        require(balances[msg.sender] >= amount, "You can not burn this much as you are poor af");
        balances[msg.sender] -= amount;
    }

    //This is a even cooler contract than ERC20 you can not only burn, but also freeze your token. 
    function freeze(uint256 amount) public
    {
        require(balances[msg.sender] >= amount, "You can not freeze this much as you are poor af");
        frozen[msg.sender] += amount;
        balances[msg.sender] -= amount;
    }

    //You can even unfreeze your token, but you can only unfreeze as much as you have frozen
    function defrost(uint256 amount) public
    {
        require(frozen[msg.sender] >= amount, "You can not unfreeze this much");
        frozen[msg.sender] -= amount;
        balances[msg.sender] += amount;
    }

    //You can even sell your token for ether, but you can only sell as much as you have
    function sell(uint256 amount) public
    {
        require(balances[msg.sender] >= amount, "You can not sell this much as you are poor af");
        uint256 new_balance = balances[msg.sender] - amount;
        (msg.sender).call{value: amount}("");
        balances[msg.sender] = new_balance;
    }

    //Internal functions (These shouldn't interest you)

    function _mint(uint256 amount, address target) internal
    {
        balances[target] += amount;
    }   
}