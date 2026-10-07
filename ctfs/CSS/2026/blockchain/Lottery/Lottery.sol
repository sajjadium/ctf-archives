// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/// @title Lottery — predict the unpredictable, ten times in a row.
contract Lottery {
    uint256 public constant STREAK_TO_WIN = 10;

    mapping(address => uint256) public streaks;
    address public winner;

    event Guessed(address indexed guesser, uint256 target, bool correct);

    /// @notice A totally random number, sourced from the blockchain itself.
    function random() public view returns (uint256) {
        return uint256(
            keccak256(
                abi.encodePacked(
                    blockhash(block.number - 1),
                    block.timestamp,
                    block.difficulty
                )
            )
        );
    }

    function guess(uint256 _guess) external {
        uint256 target = random() % 100;
        bool correct = _guess == target;

        if (correct) {
            streaks[msg.sender] += 1;
            if (streaks[msg.sender] >= STREAK_TO_WIN) {
                winner = msg.sender;
            }
        } else {
            streaks[msg.sender] = 0;
        }

        emit Guessed(msg.sender, target, correct);
    }
}
