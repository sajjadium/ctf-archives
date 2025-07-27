// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.19;

contract Arena {
    address public immutable parkContract;

    uint256 public constant PRIZE_MONEY = 0.1 ether;
    uint256 public constant PLAYER_STRENGTH = 470;
    uint256 public parkRaptorStrength = 500;

    enum FightMode { Normal, Ranked }

    mapping(address => bool) public isFighting;
    mapping(address => bool) public champions;

    constructor(address _park) payable {
        parkContract = _park;
    }

    function prepareArena() internal view {
        uint256 currentBalance = address(this).balance;
        require(currentBalance >= 0.2 ether, "Capital Audit: Stage 1 Failed.");
        require(currentBalance >= 0.4 ether, "Capital Audit: Stage 2 Failed.");
        require(currentBalance >= 0.6 ether, "Capital Audit: Stage 3 Failed.");
    }

    function triggerMeteorShower() external {
        require(msg.sender == parkContract, "Only the park can trigger events! ;)");
        parkRaptorStrength += 200;
    }

    function fight(uint8 guess, FightMode mode) external {
        if (!isFighting[msg.sender]) {
            prepareArena();
            isFighting[msg.sender] = true;
        }

        bool playerWins = _didPlayerWin(guess, mode);

        if (playerWins) {
            champions[msg.sender] = true;
            (bool sent, ) = msg.sender.call{value: PRIZE_MONEY}("");
            require(sent, "Arena: Failed to send prize");
        }

        isFighting[msg.sender] = false;
    }

    function _didPlayerWin(uint8 guess, FightMode mode) internal view returns (bool) {
        uint256 raptor = parkRaptorStrength;
        if (mode == FightMode.Ranked) {
            raptor += 100;
        }

        uint8 roll = uint8(uint256(keccak256(abi.encodePacked(block.timestamp, block.prevrandao))) % 100);

        uint256 totalPlayer = PLAYER_STRENGTH + roll;
        return (guess == roll) && (totalPlayer > raptor);
    }

    function isChampion(address _player) external view returns (bool) {
        return champions[_player];
    }

    function drainToChampion(address champ) external {
        require(msg.sender == parkContract, "Only DinoPark can drain");
        uint256 bal = address(this).balance;
        (bool ok, ) = champ.call{value: bal}("");
        require(ok, "Drain failed");
    }
}
