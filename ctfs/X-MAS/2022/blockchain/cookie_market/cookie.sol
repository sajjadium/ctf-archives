
// SPDX-License-Identifier: MIT
pragma solidity 0.8.17;

import "./ERC721.sol";

contract Cookie is ERC721("cookie", "E") {

    uint256 public cookieIDX;
    address public owner;

    constructor(){
        cookieIDX = 0;
    }

    // @dev mints an cookie. Note that there are only 10 cookies in the basket.
    function mintcookie() external {
        require(cookieIDX < 10);
        _mint(msg.sender, cookieIDX);
        cookieIDX += 1;
    }

}