// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.19;

import "@openzeppelin-upgradeable/token/ERC721/extensions/ERC721EnumerableUpgradeable.sol";
import "@openzeppelin-upgradeable/token/ERC1155/IERC1155ReceiverUpgradeable.sol";
import "./OwnedUpgradeable.sol";
import "./Interfaces.sol";
import "./Constants.sol";
import "./Randomness.sol";
import "./NFTRenderer.sol";

contract NFT is INFT, ERC721EnumerableUpgradeable, OwnedUpgradeable, IERC1155ReceiverUpgradeable {
    error InvalidItemShopContract();
    error InvalidFightTokenId();
    error OngoingFight();

    IFactory internal immutable factory;
    Randomness public randomness;
    uint40 internal _lastRequestedRandomnessTimestamp;
    address[] public pendingMintReceivers;
    mapping(uint256 tokenId => Trait) internal _traits;
    mapping(uint256 tokenId => mapping(EquipmentSlot => uint40 value)) internal _equipments;
    bytes32 internal _lastOffchainSeed;
    Fight internal _fight;

    constructor() {
        factory = IFactory(msg.sender);
    }

    function initialize(bytes calldata initialization) external initializer {
        (string memory name, string memory symbol) = abi.decode(initialization, (string, string));

        __Owned_init(address(factory));
        __ERC721_init(name, symbol);

        randomness = new Randomness();

        // create dragon boss
        uint256 tokenId = totalSupply();
        _traits[tokenId] = Trait({
            rarity: type(uint16).max,
            strength: type(uint40).max,
            dexterity: type(uint40).max / 2,
            constitution: type(uint40).max - 1,
            intelligence: type(uint40).max - 1,
            wisdom: type(uint40).max,
            charisma: 0,
            level: 60
        });
        _mint(address(this), tokenId);
    }

    function transferOwnership(address to) public override(INFT, OwnedUpgradeable) {
        OwnedUpgradeable.transferOwnership(to);
    }

    function batchMint(address[] calldata receivers) external {
        for (uint256 i = 0; i < receivers.length; i++) {
            pendingMintReceivers.push(receivers[i]);
        }

        if (pendingMintReceivers.length > 0) {
            _requestOffchainRandomness();
        }
    }

    function equip(uint256 tokenId, address itemShop, uint256 itemId) external {
        if (ownerOf(tokenId) != msg.sender) revert Unauthorized(msg.sender);
        if (!factory.isItemShopApprovedByFactory(itemShop)) {
            revert InvalidItemShopContract();
        }

        ItemInfo memory item = IItemShop(itemShop).itemInfo(itemId);
        IItemShop(itemShop).burn(msg.sender, itemId, 1);

        _equipments[tokenId][item.slot] = item.value;
    }

    function fight(uint128 attackerTokenId, uint128 attackeeTokenId) external {
        if (ownerOf(attackerTokenId) != msg.sender) revert Unauthorized(msg.sender);
        if (attackerTokenId == attackeeTokenId || !_exists(attackeeTokenId)) revert InvalidFightTokenId();
        if (_fight.attackerTokenId != _fight.attackeeTokenId) revert OngoingFight();

        _fight.attackerTokenId = attackerTokenId;
        _fight.attackeeTokenId = attackeeTokenId;
        _requestOffchainRandomness();
    }

    function _requestOffchainRandomness() internal {
        // request at most 1 randomness per block
        if (_lastRequestedRandomnessTimestamp != block.timestamp) {
            _lastRequestedRandomnessTimestamp = uint40(block.timestamp);
            emit RequestOffchainRandomness();
        }
    }

    function resolveRandomness(bytes32 seed) external override {
        if (msg.sender != address(factory.randomnessOperator())) {
            revert Unauthorized(msg.sender);
        }

        _lastOffchainSeed = seed;
        uint256 nextRound = _resolveMints();
        _resolveFight(nextRound);
    }

    function _generateRandomness(uint256 round) internal view returns (bytes32 rand) {
        rand = randomness.generate(_lastOffchainSeed, round + 1);
    }

    function _resolveMints() internal returns (uint256 nextRound) {
        uint256 length = pendingMintReceivers.length;
        if (length > 10) length = 10;

        if (length == 0) return 0;

        for (uint256 i = 0; i < length; i++) {
            uint256 tokenId = totalSupply();
            address receiver = pendingMintReceivers[i];

            uint256 rand = uint256(_generateRandomness(i));
            _traits[tokenId] = Trait({
                rarity: uint16(rand),
                strength: uint40(rand >> 16),
                dexterity: uint40(rand >> 56),
                constitution: uint40(rand >> 96),
                intelligence: uint40(rand >> 136),
                wisdom: uint40(rand >> 176),
                charisma: uint40(rand >> 216),
                level: 1
            });
            _safeMint(receiver, tokenId);
        }

        for (uint256 i = 0; i < length; i++) {
            pendingMintReceivers[length - 1 - i] = pendingMintReceivers[pendingMintReceivers.length - 1];
            pendingMintReceivers.pop();
        }

        if (pendingMintReceivers.length > 0) {
            // request further randomness to resolve outstanding mints
            _requestOffchainRandomness();
        }

        return length;
    }

    function _resolveFight(uint256 round) internal {
        if (_fight.attackerTokenId == _fight.attackeeTokenId) return;
        if (!_exists(_fight.attackerTokenId) || !_exists(_fight.attackeeTokenId)) {
            delete _fight;
            return;
        }

        FighterVars memory attacker = _getFighter(_fight.attackerTokenId);
        FighterVars memory attackee = _getFighter(_fight.attackeeTokenId);

        address attackerContract = ownerOf(_fight.attackerTokenId);
        uint256 attackerInputs;
        (bool ok, bytes memory data) = attackerContract.call(abi.encodeCall(IFighter.getInput, (attacker, attackee)));
        if (!ok || data.length != 32) {
            delete attacker; // reset and lose fight
        } else {
            attackerInputs = abi.decode(data, (uint256));
        }
        uint256 attackeeInputs = uint256(_generateRandomness(round));

        // fight at most 256 rounds
        for (uint256 i = 0; i < 256; i++) {
            FightInput attackerInput = (attackerInputs >> i) & 1 == 1 ? FightInput.Attack : FightInput.Defend;
            FightInput attackeeInput = (attackeeInputs >> i) & 1 == 1 ? FightInput.Attack : FightInput.Defend;

            if (attackerInput == FightInput.Attack) {
                _attack(attacker, attackee, attackeeInput);
            }
            if (attackeeInput == FightInput.Attack) {
                _attack(attackee, attacker, attackerInput);
            }
            if (attacker.health == 0 || attackee.health == 0) {
                break;
            }
        }

        if (attackee.health >= attacker.health) {
            _burn(_fight.attackerTokenId);
        } else {
            _burn(_fight.attackeeTokenId);
        }
    }

    function _attack(FighterVars memory attacker, FighterVars memory attackee, FightInput attackeeInput)
        internal
        pure
    {
        uint256 damage = subZero(attacker.attack, attackeeInput == FightInput.Attack ? 0 : attackee.defense);
        attackee.health = uint40(subZero(attackee.health, damage));
    }

    function _getFighter(uint256 tokenId) internal view returns (FighterVars memory fighter) {
        Trait memory trait = _traits[tokenId];
        fighter.attack = addMaxU40(trait.strength, _equipments[tokenId][EquipmentSlot.Weapon]);
        fighter.defense = addMaxU40(trait.constitution, _equipments[tokenId][EquipmentSlot.Shield]);
        fighter.health = trait.level;
    }

    function traits(uint256 tokenId) public view returns (Trait memory) {
        _requireMinted(tokenId);
        return _traits[tokenId];
    }

    function tokenURI(uint256 tokenId) public view virtual override returns (string memory) {
        _requireMinted(tokenId);

        return NFTRenderer.render(tokenId);
    }

    function onERC1155Received(address, address, uint256, uint256, bytes calldata)
        external
        pure
        override
        returns (bytes4)
    {
        return this.onERC1155Received.selector;
    }

    function onERC1155BatchReceived(address, address, uint256[] calldata, uint256[] calldata, bytes calldata)
        external
        pure
        override
        returns (bytes4)
    {
        return this.onERC1155BatchReceived.selector;
    }
}
