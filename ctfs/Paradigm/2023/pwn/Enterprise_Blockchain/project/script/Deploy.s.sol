// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-ctf/CTFDeployment.sol";

import "src/Challenge.sol";
import "src/bridge/Bridge.sol";
import "src/bridge/BridgedERC20.sol";

contract Deploy is CTFDeployment {
    function deploy(address system, address player) internal override returns (address challenge) {
        address relayer = getAdditionalAddress(0);

        vm.createSelectFork(vm.envString("L1_RPC"));
        vm.startBroadcast(system);
        Bridge l1Bridge = new Bridge(relayer);
        FlagToken flagToken = new FlagToken(address(l1Bridge), player);

        challenge = address(new Challenge(address(l1Bridge), address(flagToken)));
        vm.stopBroadcast();
        vm.startBroadcast(relayer);
        l1Bridge.registerRemoteBridge(78705, address(l1Bridge)); // assume bridge addresses are the same
        vm.stopBroadcast();

        vm.createSelectFork(vm.envString("L2_RPC"));
        vm.startBroadcast(system);
        Bridge l2Bridge = new Bridge(relayer);
        vm.stopBroadcast();
        vm.startBroadcast(relayer);
        l2Bridge.registerRemoteBridge(78704, address(l1Bridge));
        vm.stopBroadcast();
    }
}
