// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./USDT.sol";
import "./USDC.sol";
import "./Ketai.sol";
import "./PancakeSwap/PancakePair.sol";
import "./PancakeSwap/PancakeRouter.sol";
import "./PancakeSwap/PancakeFactory.sol";

// The goal is to have account 0xf2331a2d has 9999999 USDC.
contract Challenge {
    USDC public usdc;
    USDT public usdt;
    Ketai public ketai;

    IPancakeRouter02 public router;
    IPancakeFactory public factory;

    IPancakePair public ketaiUSDTPair;
    IPancakePair public ketaiUSDCPair;

    address public randomFolks = address(0xf2331a2d);

    constructor(PancakeFactory factory_, PancakeRouter router_) {
        factory = factory_;
        router = router_;

        // deploy tokens
        usdt = new USDT();
        ketai = new Ketai();
        usdc = new USDC();

        // create pairs for Ketai
        factory.createPair(address(usdt), address(ketai));
        ketaiUSDTPair = IPancakePair(PancakeLibrary.pairFor(address(factory), address(usdt), address(ketai)));
        factory.createPair(address(usdc), address(ketai));
        ketaiUSDCPair = IPancakePair(PancakeLibrary.pairFor(address(factory), address(usdc), address(ketai)));

        // approve router to spend token
        ketai.approve(address(router), 10000000 * 1e18);
        usdc.approve(address(router), 10000000 * 1e18);
        usdt.approve(address(router), 10000000 * 1e18);

        // add liquidity for Ketai / USDT pair
        router.addLiquidity(
            address(ketai), address(usdt),
            5000000 * 1e18,
            10000000 * 1e18,
            0,
            0,
            address(this),
            block.timestamp
        );

        // add liquidity for Ketai / USDC pair
        router.addLiquidity(
            address(ketai), address(usdc),
            5000000 * 1e18,
            10000000 * 1e18,
            0,
            0,
            address(this),
            block.timestamp
        );

        // set trading info for Ketai
        ketai.setTradingInfo(address(usdt), address(ketaiUSDTPair), address(router));
    }

    function isSolved() public view returns (bool) {
        return usdc.balanceOf(address(randomFolks)) >= 9999999 * 1e18;
    }
}
