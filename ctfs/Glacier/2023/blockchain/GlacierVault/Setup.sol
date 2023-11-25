// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./GlacierVault.sol";
import "./Guardian.sol";

contract Setup {
    Guardian public immutable TARGET; // Contract the player will hack

    constructor() payable {
        // Deploy the victim contract
        GlacierVault vault = new GlacierVault();

        // Deploy the guardian contract
        TARGET = new Guardian(address(vault));
    }

    // Our challenge in the CTF framework will call this function to
    // check whether the player has solved the challenge or not.
    function isSolved() public view returns (bool) {
        return TARGET.asleep();
    }
}