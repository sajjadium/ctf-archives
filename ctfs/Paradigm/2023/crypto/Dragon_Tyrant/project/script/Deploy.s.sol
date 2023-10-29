// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-ctf/CTFDeployment.sol";

import "src/Challenge.sol";
import "src/Factory.sol";
import "src/ItemShop.sol";
import "src/NFT.sol";

contract Deploy is CTFDeployment {
    function deploy(address system, address) internal override returns (address challenge) {
        vm.startBroadcast(system);

        Factory factory = new Factory();
        factory.setRandomnessOperator(getAdditionalAddress(0));

        ItemShop itemShop = ItemShop(factory.createItemShop(address(factory.latestItemShopVersion()), abi.encode("")));

        NFT nft = NFT(factory.createCollection(abi.encode(string("Fighters"), string("FGHTRS"))));

        challenge = address(new Challenge(factory, itemShop, nft));

        vm.stopBroadcast();
    }
}
