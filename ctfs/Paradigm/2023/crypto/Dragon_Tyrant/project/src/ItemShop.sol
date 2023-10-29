// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.19;

import "@openzeppelin-upgradeable/token/ERC1155/extensions/ERC1155BurnableUpgradeable.sol";
import "@openzeppelin-upgradeable/token/ERC1155/IERC1155ReceiverUpgradeable.sol";
import "./OwnedUpgradeable.sol";
import "./Interfaces.sol";
import "./Constants.sol";

contract ItemShop is ERC1155BurnableUpgradeable, IERC1155ReceiverUpgradeable {
    error InvalidItem();
    error InvalidAmount();

    IFactory internal immutable factory;
    mapping(uint256 tokenId => ItemInfo) internal _itemInfo;

    constructor() {
        factory = IFactory(msg.sender);
    }

    function initialize(bytes calldata initialization) external initializer {
        (string memory uri) = abi.decode(initialization, (string));

        __ERC1155_init(uri);
        __ERC1155Burnable_init();

        uint256 counter = 0;
        _itemInfo[++counter] = ItemInfo({name: "Broadsword", slot: EquipmentSlot.Weapon, value: 1 << 38, price: 1e18});
        _mint(address(this), counter, 100, "");

        _itemInfo[++counter] =
            ItemInfo({name: "Wooden Shield", slot: EquipmentSlot.Shield, value: 1 << 38, price: 1e18});
        _mint(address(this), counter, 100, "");

        _itemInfo[++counter] =
            ItemInfo({name: "Legendary Sword", slot: EquipmentSlot.Weapon, value: type(uint40).max, price: 1e6 * 1e18});
        _mint(address(this), counter, 1, "");
    }

    function buy(uint256 itemId) external payable {
        if (balanceOf(address(this), itemId) == 0) {
            revert InvalidItem();
        }

        ItemInfo storage item = _itemInfo[itemId];
        if (msg.value != item.price) revert InvalidAmount();

        _safeTransferFrom(address(this), msg.sender, itemId, 1, "");
    }

    function itemInfo(uint256 tokenId) external view returns (ItemInfo memory item) {
        item = _itemInfo[tokenId];
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
