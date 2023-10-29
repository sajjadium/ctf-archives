// SPDX-License-Identifier: Apache-2.0
pragma solidity >=0.7.0 <0.9.0;

import "forge-std/Test.sol";

import {HuffConfig} from "../HuffConfig.sol";
import {HuffDeployer} from "../HuffDeployer.sol";
import {INumber} from "./interfaces/INumber.sol";
import {IConstructor} from "./interfaces/IConstructor.sol";

contract LoggingTest is Test {
    event LogOne();
    event LogTwo(address indexed a);
    event LogThree(address indexed a, uint256 indexed b);
    event LogFour(address indexed a, uint256 indexed b, bytes32 indexed c);
    event Extended(
        address indexed a,
        uint256 indexed b,
        bytes32 indexed h1,
        bytes32 h2,
        bytes32 two
    );

    function testLoggingWithArgs() public {
        // Ignore the second topic (address) since the internal HuffConfig is the msg.sender
        vm.expectEmit(false, true, true, true);
        emit LogOne();
        emit LogTwo(address(0));
        emit LogThree(address(0), 0);
        emit LogFour(address(0), 0, keccak256(abi.encode(1)));
        emit Extended(
            address(0),
            0,
            keccak256(abi.encode(1)),
            keccak256(abi.encode(2)),
            keccak256(abi.encode(3))
            );
        HuffDeployer.deploy_with_args(
            "test/contracts/LotsOfLogging",
            bytes.concat(abi.encode(address(0x420)), abi.encode(uint256(0x420)))
        );
    }

    function testLoggingWithDeploy() public {
        vm.expectEmit(false, true, true, true);
        emit LogOne();
        emit LogTwo(address(0));
        emit LogThree(address(0), 0);
        emit LogFour(address(0), 0, keccak256(abi.encode(1)));
        emit Extended(
            address(0),
            0,
            keccak256(abi.encode(1)),
            keccak256(abi.encode(2)),
            keccak256(abi.encode(3))
            );
        HuffDeployer.deploy("test/contracts/LotsOfLogging");
    }

    function testConfigLogging() public {
        HuffConfig config =
            HuffDeployer.config().with_args(abi.encode(address(0x420)));
        vm.expectEmit(true, true, true, true);
        emit LogOne();
        emit LogTwo(address(config));
        emit LogThree(address(config), 0);
        emit LogFour(address(config), 0, keccak256(abi.encode(1)));
        emit Extended(
            address(config),
            0,
            keccak256(abi.encode(1)),
            keccak256(abi.encode(2)),
            keccak256(abi.encode(3))
            );
        config.deploy("test/contracts/LotsOfLogging");
    }
}
