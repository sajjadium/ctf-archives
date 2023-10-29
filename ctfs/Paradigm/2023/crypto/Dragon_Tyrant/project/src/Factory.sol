// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "@openzeppelin/token/ERC721/extensions/ERC721Enumerable.sol";
import "./OwnedUpgradeable.sol";
import "./NFT.sol";
import "./Randomness.sol";
import "./ItemShop.sol";

contract Factory is IFactory, OwnedUpgradeable {
    error InvalidCodehash();

    mapping(bytes32 => bool) public approvedItemShopCodehashes;
    address public latestItemShopVersion;
    address public randomnessOperator;

    constructor() {
        __Owned_init(msg.sender);

        address itemShopBluePrint = address(new ItemShop());
        _setApprovedItemShopImplementation(itemShopBluePrint, true);
    }

    function createCollection(bytes calldata initialization) external returns (address nft) {
        nft = address(new NFT());
        INFT(nft).initialize(initialization);
        INFT(nft).transferOwnership(msg.sender);
    }

    function createItemShop(address implementation, bytes calldata initialization)
        external
        returns (address itemShop)
    {
        bytes32 codehash;
        assembly {
            codehash := extcodehash(implementation)
        }
        if (!approvedItemShopCodehashes[codehash]) revert InvalidCodehash();
        itemShop = _clone(implementation);
        IItemShop(itemShop).initialize(initialization);
    }

    function isItemShopApprovedByFactory(address itemShop) external view returns (bool) {
        bytes32 codehash;
        assembly {
            codehash := extcodehash(itemShop)
        }
        return approvedItemShopCodehashes[codehash];
    }

    function setApprovedItemShopImplementation(address implementation, bool approved) external onlyOwner {
        _setApprovedItemShopImplementation(implementation, approved);
    }

    function _setApprovedItemShopImplementation(address implementation, bool approved) internal {
        bytes32 codehash;
        assembly {
            codehash := extcodehash(implementation)
        }
        approvedItemShopCodehashes[codehash] = approved;
        latestItemShopVersion = implementation;
    }

    function setRandomnessOperator(address operator) external onlyOwner {
        randomnessOperator = operator;
    }

    function _clone(address a) internal returns (address) {
        // from https://gist.github.com/holiman/069de8d056a531575d2b786df3345665
        address retval;
        assembly {
            mstore(
                0x0,
                or(0x5880730000000000000000000000000000000000000000803b80938091923cF3, mul(a, 0x1000000000000000000))
            )
            retval := create(0, 0, 32)
        }
        return retval;
    }
}
