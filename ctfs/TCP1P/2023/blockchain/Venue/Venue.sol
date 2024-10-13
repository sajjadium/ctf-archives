// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract Venue{
    string private flag;
    string private message;

    constructor(string memory initialFlag, string memory initialMessage){
        flag = initialFlag;
        message = initialMessage;
    }

    function enterVenue() public view returns(string memory){
        return flag;
    }

    function goBack() public view returns(string memory){
        return message;
    }
}