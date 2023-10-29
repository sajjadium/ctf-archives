// SPDX-License-Identifier: BSD
pragma solidity ^0.8.4;

import {DSTest} from "ds-test/test.sol";

import {Hevm} from "./utils/Hevm.sol";
import {ExampleClone} from "../ExampleClone.sol";
import {ExampleCloneFactory} from "../ExampleCloneFactory.sol";

contract ExampleCloneFactoryTest is DSTest {
    Hevm internal constant hevm = Hevm(HEVM_ADDRESS);

    ExampleCloneFactory internal factory;

    function setUp() public {
        ExampleClone implementation = new ExampleClone();
        factory = new ExampleCloneFactory(implementation);
    }

    /// -----------------------------------------------------------------------
    /// Gas benchmarking
    /// -----------------------------------------------------------------------

    function testGas_clone(
        address param1,
        uint256 param2,
        uint64 param3,
        uint8 param4
    ) public {
        factory.createClone(param1, param2, param3, param4);
    }

    /// -----------------------------------------------------------------------
    /// Correctness tests
    /// -----------------------------------------------------------------------

    function testCorrectness_clone(
        address param1,
        uint256 param2,
        uint64 param3,
        uint8 param4
    ) public {
        ExampleClone clone = factory.createClone(
            param1,
            param2,
            param3,
            param4
        );
        assertEq(clone.param1(), param1);
        assertEq(clone.param2(), param2);
        assertEq(clone.param3(), param3);
        assertEq(clone.param4(), param4);
    }
}
