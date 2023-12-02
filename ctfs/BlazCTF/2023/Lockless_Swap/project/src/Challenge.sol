// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./ERC20.sol";
import "./LocklessPancakePair.sol";

contract Token0 is ERC20, Ownable {
    constructor() ERC20("Token0", "Token0") {
        _mint(msg.sender, 100 * 1e18);
    }
}

contract Token1 is ERC20, Ownable {
    constructor() ERC20("Token1", "Token1") {
        _mint(msg.sender, 100 * 1e18);
    }
}

contract Challenge {
    ERC20 public token0;
    ERC20 public token1;

    PancakePair public pair;

    address public randomFolks = address(0xf2331a2d);

    constructor(address) {
        // deploy tokens
        token0 = new Token0();
        token1 = new Token1();

        // create pairs for token1 / token2
        pair = new PancakePair();
        pair.initialize(address(token0), address(token1));

        // add liquidity for the pair
        token0.transfer(address(pair), 99 * 1e18);
        token1.transfer(address(pair), 99 * 1e18);
        pair.mint(address(this));
    }

    function faucet() public {
        token0.transfer(msg.sender, 1 * 1e18);
        token1.transfer(msg.sender, 1 * 1e18);
    }

    function isSolved() public view returns (bool) {
        return
            token1.balanceOf(address(randomFolks)) >= 99 * 1e18 && token0.balanceOf(address(randomFolks)) >= 99 * 1e18;
    }
}
