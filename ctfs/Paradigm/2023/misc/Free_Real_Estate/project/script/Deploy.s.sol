// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-ctf/CTFDeployment.sol";

import "src/Challenge.sol";
import "src/InuToken.sol";
import "@uniswap/merkle-distributor/contracts/MerkleDistributor.sol";

contract Deploy is CTFDeployment {
    function deploy(address system, address) internal override returns (address challenge) {
        bytes32 merkleRoot = vm.envBytes32("MERKLE_ROOT");
        uint256 tokenTotal = vm.envUint("TOKEN_TOTAL");

        vm.startBroadcast(system);

        InuToken token = new InuToken();
        MerkleDistributor distributor = new MerkleDistributor(address(token), merkleRoot);
        token.transfer(address(distributor), tokenTotal);

        challenge = address(new Challenge(distributor));

        vm.stopBroadcast();
    }
}
