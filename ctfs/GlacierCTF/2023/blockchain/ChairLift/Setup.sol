// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./ChairLift.sol";

contract Setup {
    ChairLift public immutable TARGET; // Contract the player will hack

    constructor() payable {
        require(msg.value == 100 ether);

        // Deploy the victim contract
        TARGET = new ChairLift();

        // Check if buying a ticket works
        TARGET.buyTicket();

        // Check if taking a ride works
        TARGET.takeRide(0);
    }

    // Our challenge in the CTF framework will call this function to
    // check whether the player has solved the challenge or not.
    function isSolved() public view returns (bool) {
        return TARGET.tripsTaken() == 2;
    }
}