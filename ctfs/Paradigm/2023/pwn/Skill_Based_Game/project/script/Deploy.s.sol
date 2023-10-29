// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "forge-ctf/CTFDeployment.sol";
import "../src/Challenge.sol";

contract Deploy is CTFDeployment {
    address private immutable BLACKJACK = 0xA65D59708838581520511d98fB8b5d1F76A96cad;

    function deploy(address system, address) internal override returns (address challenge) {
        vm.startBroadcast(system);

        payable(BLACKJACK).transfer(50 ether);
        challenge = address(new Challenge(BLACKJACK));

        vm.stopBroadcast();
    }
}
