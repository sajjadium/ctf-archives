// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./respectToken.sol";
import "./candyToken.sol";

/// @notice Gang respects you if you give them treats
contract localGang{

    candyToken public immutable candy;
    respectToken public immutable respect;
    mapping (address=>uint) public candyCount;

    constructor(address candyAddress, address respectAddress){
        candy = candyToken(candyAddress);
        respect = respectToken(respectAddress);
    }

    function gainRespect(uint _candyCount) public payable{

        require(_candyCount!=0, "You need donate candies to gain respect");
        require(candy.balanceOf(msg.sender)>=_candyCount, "You don't have enough candies");
        require(candy.allowance(msg.sender, address(this))>=_candyCount, "You need to approve the contract to transfer candies");

        candyCount[msg.sender] += _candyCount;
        candy.transferFrom(msg.sender, address(this), _candyCount);

        respect.mint(msg.sender, _candyCount);
    }

    function loseRespect(uint _respectCount) public payable{
        require(_respectCount!=0, "You need to lose respect to get back your candies");
        require(respect.balanceOf(msg.sender)>=_respectCount, "You don't have enough respect");
        require(respect.allowance(msg.sender, address(this))>=_respectCount, "You need to approve the contract to transfer respect");

        respect.burn(address(msg.sender), _respectCount);

        candyCount[msg.sender] -= _respectCount;
        candy.transfer(msg.sender, _respectCount);

    }
    
}