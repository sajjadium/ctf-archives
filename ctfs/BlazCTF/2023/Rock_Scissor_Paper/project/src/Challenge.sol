// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract RockPaperScissors {
    bool public defeated;

    enum Hand {
        Rock,
        Paper,
        Scissors
    }

    function randomShape() internal view returns (Hand) {
        return Hand(uint256(keccak256(abi.encodePacked(msg.sender, blockhash(block.number - 1)))) % 3);
    }

    function tryToBeatMe(Hand yours) external payable {
        Hand mine = randomShape();

        if (yours == Hand.Rock && mine == Hand.Scissors) {
            defeated = true;
        } else if (yours == Hand.Paper && mine == Hand.Rock) {
            defeated = true;
        } else if (yours == Hand.Scissors && mine == Hand.Paper) {
            defeated = true;
        }
    }
}

contract Challenge {
    address public immutable PLAYER;
    RockPaperScissors public immutable rps;

    constructor(address player) {
        PLAYER = player;
        rps = new RockPaperScissors();
    }

    function isSolved() external view returns (bool) {
        return rps.defeated();
    }
}
