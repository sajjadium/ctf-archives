// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-ctf/CTFDeployment.sol";
import "src/Challenge.sol";
import "src/Router.sol";

contract Deploy is CTFDeployment {
    function deploy(address system, address) internal override returns (address challenge) {
        vm.startBroadcast(system);

        Router router = new Router();

        challenge = address(new Challenge(address(router)));

        vm.stopBroadcast();
    }
}
