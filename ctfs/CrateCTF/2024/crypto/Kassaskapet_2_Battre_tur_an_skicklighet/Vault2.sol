// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Vault2 {
    address public p;
    uint256 internal lastBlock;
    uint8 public acesInRow;
    // setting owner to your wallet address will allow you to claim the flag on challs.crate.nu:50006
    address public owner;

    constructor(address player) {
        p = player;
        acesInRow = 0;
        owner = msg.sender;
    }

    function _random() internal view returns(uint8) {
        uint256 bn1 = uint256(blockhash(block.number - 1));
        uint256 bn2 = uint256(blockhash(block.number));
        return uint8(((bn1) ^ (bn2)) % 52);
    }

    function drawCard() external payable{
        require(msg.value > 0.01 ether);
        require(tx.origin != msg.sender);
        require(p == tx.origin, "Unknown player tried to Claim");
        require(block.number != lastBlock, "too early");
        lastBlock = block.number;

        uint8 card = _random();
        if (card % 13 == 0) {
            acesInRow += 1;
        } else {
            acesInRow = 0;
        }
    }
    function unlock() external payable {
        require(msg.value > 0.1 ether);
        require(tx.origin != msg.sender);
        require(acesInRow >= 10, "Not enough rounds won in a row");
        require(p == tx.origin, "Unknown player tried to Claim");
        owner = tx.origin;
    }
}
