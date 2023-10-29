// SPDX-License-Identifier: Apache-2.0
pragma solidity >=0.7.0 <0.9.0;

import "forge-std/Test.sol";

import {INumber} from "./interfaces/INumber.sol";
import {IConstructor} from "./interfaces/IConstructor.sol";
import {HuffConfig} from "../HuffConfig.sol";

contract HuffConfigTest is Test {
    HuffConfig public config;
    INumber public number;

    function setUp() public {
        config = new HuffConfig();
    }

    function testWithArgs(bytes memory some) public {
        config.with_args(some);
        assertEq(config.args(), some);
    }

    function testWithValue(uint256 value) public {
        config.with_value(value);
        assertEq(config.value(), value);
    }

    function testWithCode(string memory code) public {
        config.with_code(code);
        assertEq(config.code(), code);
    }

    function testWithConstantOverrides(
        string memory key,
        string memory value
    ) public {
        config.with_constant(key, value);
        (string memory k, string memory v) = config.const_overrides(0);
        assertEq(key, k);
        assertEq(value, v);
    }

    function testSetBroadcast(bool broadcast) public {
        config.set_broadcast(broadcast);
        bool b = config.should_broadcast();
        assertEq(b, broadcast);
    }
}
