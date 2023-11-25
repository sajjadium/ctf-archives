// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Challenge.sol";

contract Setup {
    GlacierCoin public immutable TARGET; // Contract the player will hack

    constructor() payable {
        require(msg.value == 100 ether);

        // Deploy the victim contract
        TARGET = new GlacierCoin();

        // Send 10 ether to the victim contract as initial balance
        TARGET.buy{value: 10 ether}();
    }

    // Our challenge in the CTF framework will call this function to
    // check whether the player has solved the challenge or not.
    function isSolved() public view returns (bool) {
        return address(TARGET).balance == 0;
    }
}