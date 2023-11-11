pragma solidity ^0.8.16;

import "./Bank.sol";

contract Setup {
    
    Bank public immutable challenge;

    constructor() {
        challenge = new Bank();
    }
    
    function isSolved() public view returns (bool) {
        return address(challenge).balance == 0;
    }
}
