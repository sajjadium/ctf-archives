// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-ctf/CTFDeployment.sol";

import "src/Challenge.sol";

interface BridgeLike {
    function sendToL2(
        uint256 chainId,
        address recipient,
        uint256 amount,
        uint256 amountOutMin,
        uint256 deadline,
        address relayer,
        uint256 relayerFee
    ) external payable;

    function governance() external view returns (address);

    function setGovernance(address) external;
}

contract Deploy is CTFDeployment {
    BridgeLike private immutable BRIDGE = BridgeLike(0xb8901acB165ed027E32754E0FFe830802919727f);

    function deploy(address system, address player) internal override returns (address challenge) {
        address governance = BRIDGE.governance();

        vm.startBroadcast(system);

        payable(governance).transfer(1 ether);

        BRIDGE.sendToL2{value: 900 ether}(10, system, 900 ether, 0, 0, address(0x00), 0);

        challenge = address(new Challenge(address(BRIDGE)));

        vm.stopBroadcast();

        vm.startBroadcast(governance);

        BRIDGE.setGovernance(player);

        vm.stopBroadcast();
    }
}
