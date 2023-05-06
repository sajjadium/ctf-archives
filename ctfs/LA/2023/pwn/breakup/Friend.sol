// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.18;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract Friend is ERC721Enumerable, Ownable {
    using Counters for Counters.Counter;

    Counters.Counter private _uuidCounter;
    mapping(uint256 => string) public friendNames;

    constructor() ERC721("Friend", "FRN") {}

    function safeMint(address to, string calldata name) public {
        _uuidCounter.increment();
        uint256 tokenId = _uuidCounter.current();
        _safeMint(to, tokenId);
        friendNames[tokenId] = name;
    }

    function burn(uint256 tokenId) public {
        _burn(tokenId);
        delete friendNames[tokenId];
    }

    function friend(string calldata name) public {
        bytes memory nameBytes = bytes(name);
        uint256 totalFriends = balanceOf(msg.sender);
        for (uint256 i = 0; i < totalFriends; i++) {
            bytes memory thisNameBytes = bytes(friendNames[tokenOfOwnerByIndex(msg.sender, i)]);
            if (
                nameBytes.length == thisNameBytes.length &&
                (nameBytes.length == 0 || keccak256(nameBytes) == keccak256(thisNameBytes))
            ) {
                revert("You're already friends with that person!");
            }
        }

        safeMint(msg.sender, name);
    }

    function unfriend(string calldata name) public {
        bytes memory nameBytes = bytes(name);
        uint256 totalFriends = balanceOf(msg.sender);
        for (uint256 i = 0; i < totalFriends; i++) {
            uint256 tokenId = tokenOfOwnerByIndex(msg.sender, i);
            bytes memory thisNameBytes = bytes(friendNames[tokenId]);
            if (
                nameBytes.length == thisNameBytes.length &&
                (nameBytes.length == 0 || keccak256(nameBytes) == keccak256(thisNameBytes))
            ) {
                burn(tokenId);
                return;
            }
        }

        revert("You weren't friends with that person anyways.");
    }
}
