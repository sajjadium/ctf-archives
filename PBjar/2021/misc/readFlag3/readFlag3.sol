// SPDX-License-Identifier: MIT
pragma solidity ^0.8.3;

contract readFlag3 {
    string private flag = "REDACTED";
    address public owner;

    constructor(string memory _flagVal) {

        owner = msg.sender;
        flag = _flagVal;
    }

    function get() public view returns (string memory) {
        require(msg.sender == owner, "This can only be called by the contract owner!");
        return flag;
    }
}
