// SPDX-License-Identifier: UNLICENSED

// DO NOT RELEASE SOURCE FOR THIS CHAL IT'S A REVERSING CHALLENGE.
//
// Challenge author: stong (cts), Zellic Inc.
// Challenge prepared for Paradigm CTF 2022

pragma solidity 0.8.16;

import "Challenge.sol";

interface ChallengeInterface {
    function solved() external view returns (bool);
}

contract Setup {
    ChallengeInterface public challenge;
    
    constructor() {        
        challenge = ChallengeInterface(address(new Challenge()));
    }
    
    function isSolved() public view returns (bool) {
        return challenge.solved();
    }
}