// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Chal {
    address public owner;
    uint public player_tokens;
    uint public dealer_tokens;
    uint public playerCardsValue;
    bool public game_on;
    uint public dealerCardsValue;

    constructor() {
        owner = msg.sender;
        player_tokens = 1;
        dealer_tokens = 1;
        playerCardsValue = 0;
        game_on = false;
        dealerCardsValue = 20;
    }

    function start_game() external payable {
        require(player_tokens >= 0, "Player has lost all their tokens" );
        require(game_on == false, "Player is already in the game");

        game_on = true;
    }

    function hit() external {
        require(game_on == true, "Player not in the game");
        require(playerCardsValue < 22, "Player has already won or busted");

        uint256 blockValue = uint256(blockhash(block.number - 1));
        uint cardValue = (blockValue % 5) + 1;

        playerCardsValue += cardValue;

        if (playerCardsValue > 22) {
            player_tokens -= 1;
            dealer_tokens += 1;
            game_on = false;
            playerCardsValue = 0;
        }
        else if (playerCardsValue > dealerCardsValue) {
            player_tokens += 1;
            dealer_tokens -= 1;
            game_on = false;
            playerCardsValue = 0;
        }
    }

    function get_player_tokens() external view returns (uint) {
        return player_tokens;
    }

    function get_dealer_tokens() external view returns (uint) {
        return dealer_tokens;
    }

    function getCardsValue() external view returns (uint) {
        return playerCardsValue;
    }
}