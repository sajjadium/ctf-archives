// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Vault {

    bool public paused;      
    uint248 public fee;      

    address public admin;    
    address public governance;

    constructor() payable {
        paused = true;
        admin = msg.sender;
    }

    function execute(bytes calldata data) public {
    (bool ok,) = governance.delegatecall(data);
    require(ok);
    }

    function withdraw() public {
        require(!paused, "paused");
        require(msg.sender == admin, "not admin");

        payable(msg.sender).transfer(address(this).balance);
    }
    
    function setGovernance(address _g) public {
    governance = _g;
    }

    function getBalance() public view returns(uint){
        return address(this).balance;
    }
    function isSolved() public view returns(bool) {
    return address(this).balance == 0;
    }
}