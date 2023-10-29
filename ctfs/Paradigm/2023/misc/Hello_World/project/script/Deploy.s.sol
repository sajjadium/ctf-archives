// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-ctf/CTFDeployment.sol";

import "src/Challenge.sol";

contract Deploy is CTFDeployment {
    function deploy(address system, address) internal override returns (address challenge) {
        vm.startBroadcast(system);

        challenge = address(new Challenge());

        vm.stopBroadcast();
    }
}
