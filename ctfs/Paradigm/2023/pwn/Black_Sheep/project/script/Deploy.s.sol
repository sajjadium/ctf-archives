// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-ctf/CTFDeployment.sol";

import "foundry-huff/HuffConfig.sol";

import "src/Challenge.sol";
import "src/ISimpleBank.sol";

contract Deploy is CTFDeployment {
    function deploy(address system, address) internal override returns (address challenge) {
        HuffConfig config = new HuffConfig();
        config.set_broadcast(true);

        ISimpleBank bank = ISimpleBank(config.deploy("SimpleBank"));

        vm.startBroadcast(system);

        payable(address(bank)).transfer(10 ether);

        challenge = address(new Challenge(bank));

        vm.stopBroadcast();
    }
}
