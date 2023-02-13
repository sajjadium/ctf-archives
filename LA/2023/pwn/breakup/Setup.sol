// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.18;

import "@openzeppelin/contracts/token/ERC721/IERC721Receiver.sol";
import "./Friend.sol";

contract Setup {
    Friend public immutable friend;
    SomebodyYouUsedToKnow public immutable somebodyYouUsedToKnow;

    constructor() {
        friend = new Friend();
        somebodyYouUsedToKnow = new SomebodyYouUsedToKnow(friend);
    }

    function isSolved() external view returns (bool) {
        uint256 totalFriends = friend.balanceOf(address(somebodyYouUsedToKnow));
        if (totalFriends == 0) {
            return true;
        }

        bytes memory you = "You";
        for (uint256 i = 0; i < totalFriends; i++) {
            bytes memory thisNameBytes = bytes(
                friend.friendNames(friend.tokenOfOwnerByIndex(address(somebodyYouUsedToKnow), i))
            );
            if (you.length == thisNameBytes.length && keccak256(you) == keccak256(thisNameBytes)) {
                return false;
            }
        }

        return true;
    }
}

contract SomebodyYouUsedToKnow is IERC721Receiver {
    constructor(Friend friend) {
        friend.friend("You");
    }

    function onERC721Received(
        address,
        address,
        uint256,
        bytes calldata
    ) external pure override returns (bytes4) {
        return IERC721Receiver.onERC721Received.selector;
    }
}
