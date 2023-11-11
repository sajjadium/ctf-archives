pragma solidity ^0.8.20;

import "./DrainMeBaby.sol";


contract Setup {
    DrainMeBaby public immutable challenge;

    constructor() payable {
        require(msg.value == 100 ether, "Not enough balance for target contract");
        challenge = new DrainMeBaby();
        challenge.deposit{value: 100 ether}();
    }

    function isSolved() public view returns (bool) {
        return challenge.getBalance() == 0 ether;
    }

    // Helper function to check the balance of this contract
    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
}
