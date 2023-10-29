// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-ctf/CTFDeployment.sol";

import "src/Split.sol";
import "src/Challenge.sol";

contract Deploy is CTFDeployment {
    function deploy(address system, address) internal override returns (address challenge) {
        vm.startBroadcast(system);

        Split split = new Split();

        address[] memory addrs = new address[](2);
        addrs[0] = address(0x000000000000000000000000000000000000dEaD);
        addrs[1] = address(0x000000000000000000000000000000000000bEEF);
        uint32[] memory percents = new uint32[](2);
        percents[0] = 5e5;
        percents[1] = 5e5;

        uint256 id = split.createSplit(addrs, percents, 0);

        Split.SplitData memory splitData = split.splitsById(id);
        splitData.wallet.deposit{value: 100 ether}();

        challenge = address(new Challenge(split));

        vm.stopBroadcast();
    }
}
