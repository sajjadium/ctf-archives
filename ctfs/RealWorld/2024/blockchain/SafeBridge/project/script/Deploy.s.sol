pragma solidity ^0.8.20;

import {Script} from "forge-std/Script.sol";

import "src/L1/WETH.sol";
import "src/L1/L1CrossDomainMessenger.sol";
import "src/L1/L1ERC20Bridge.sol";
import "src/Challenge.sol";

import {Lib_PredeployAddresses} from "src/libraries/constants/Lib_PredeployAddresses.sol";

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Deploy is Script {
    function setUp() public {}

    function run() public {
        address system = getAddress(1);

        address challenge = deploy(system);

        vm.writeFile(vm.envOr("OUTPUT_FILE", string("/tmp/deploy.txt")), vm.toString(challenge));
    }

    function deploy(address system) internal returns (address challenge) {
        vm.createSelectFork(vm.envString("L1_RPC"));
        vm.startBroadcast(system);
        address relayer = getAdditionalAddress(0);
        L1CrossDomainMessenger l1messenger = new L1CrossDomainMessenger(relayer);
        WETH weth = new WETH();
        L1ERC20Bridge l1Bridge =
            new L1ERC20Bridge(address(l1messenger), Lib_PredeployAddresses.L2_ERC20_BRIDGE, address(weth));

        weth.deposit{value: 2 ether}();
        weth.approve(address(l1Bridge), 2 ether);
        l1Bridge.depositERC20(address(weth), Lib_PredeployAddresses.L2_WETH, 2 ether);

        challenge = address(new Challenge(address(l1Bridge), address(l1messenger), address(weth)));
        vm.stopBroadcast();
    }

    function getAdditionalAddress(uint32 index) internal returns (address) {
        return getAddress(index + 2);
    }

    function getPrivateKey(uint32 index) private returns (uint256) {
        string memory mnemonic =
            vm.envOr("MNEMONIC", string("test test test test test test test test test test test junk"));
        return vm.deriveKey(mnemonic, index);
    }

    function getAddress(uint32 index) private returns (address) {
        return vm.addr(getPrivateKey(index));
    }
}
