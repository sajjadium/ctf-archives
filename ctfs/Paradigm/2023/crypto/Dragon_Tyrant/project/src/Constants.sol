// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.19;

import "@openzeppelin-upgradeable/token/ERC721/extensions/ERC721EnumerableUpgradeable.sol";
import "./OwnedUpgradeable.sol";
import "./Interfaces.sol";

struct Trait {
    uint16 rarity;
    uint40 strength;
    uint40 dexterity;
    uint40 constitution;
    uint40 intelligence;
    uint40 wisdom;
    uint40 charisma;
    uint8 level;
}

enum EquipmentSlot {
    Weapon,
    Shield
}

enum FightInput {
    Attack,
    Defend
}

struct Fight {
    uint128 attackerTokenId;
    uint128 attackeeTokenId;
}

struct FighterVars {
    uint40 attack;
    uint40 defense;
    uint40 health;
}

struct ItemInfo {
    string name;
    EquipmentSlot slot;
    uint40 value;
    uint80 price;
}

function subZero(uint256 a, uint256 b) pure returns (uint256) {
    if (b > a) return 0;
    return a - b;
}

function addMaxU40(uint40 a, uint40 b) pure returns (uint40) {
    uint256 sum = uint256(a) + b;
    return sum > type(uint40).max ? type(uint40).max : uint40(sum);
}
