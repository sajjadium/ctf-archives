// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "forge-ctf/CTFDeployer.sol";

import "src/Challenge.sol";

contract Deploy is CTFDeployer {
    function deploy(address system, address player) internal override returns (address challenge) {
        vm.startBroadcast(system);

        // deploy pancakeswap factory and router
        PancakeFactory factory = new PancakeFactory(address(this));
        PancakeRouter router = new PancakeRouter(address(factory), address(0));

        challenge = address(new Challenge(factory, router));

        vm.stopBroadcast();
    }
}
