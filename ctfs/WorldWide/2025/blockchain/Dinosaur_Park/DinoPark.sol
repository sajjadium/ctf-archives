// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.19;

import "./Arena.sol";

contract DinoPark {
    address public owner;
    address public goldenEggHolder;
    Arena public arena;

    mapping(address => uint256) public patronStake;
    mapping(uint256 => string) public dinoNames;
    uint256 public constant NAMING_FEE = 0.01 ether;

    constructor() payable {
        owner = msg.sender;
        goldenEggHolder = address(this);
        arena = new Arena{value: 0.5 ether}(address(this));
    }

    function announceMeteorShower() external {
        require(msg.sender == owner, "Only the owner can make announcements.");
        arena.triggerMeteorShower();
    }

    function claimGoldenEgg() external {
        require(arena.isChampion(msg.sender), "DinoPark: Not a champion!");
        require(address(arena).balance <= 1 wei, "DinoPark: Arena still has funds!");
        goldenEggHolder = msg.sender;
    }

    function stakeForPark() external payable {
        patronStake[msg.sender] += msg.value;
    }

    function withdrawStake() external {
        uint256 amount = patronStake[msg.sender];
        require(amount > 0, "No stake to withdraw.");
        patronStake[msg.sender] = 0;
        (bool sent, ) = msg.sender.call{value: amount}("");
        require(sent, "Withdrawal failed.");
    }

    function setDinoName(uint256 dinoId, string calldata name) external payable {
        require(msg.value == NAMING_FEE, "Incorrect fee for naming service.");
        dinoNames[dinoId] = name;
    }

    function isSolved() external view returns (bool) {
        return goldenEggHolder == msg.sender;   
    }
}
