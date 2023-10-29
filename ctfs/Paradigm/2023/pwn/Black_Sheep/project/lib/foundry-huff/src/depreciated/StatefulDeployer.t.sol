// SPDX-License-Identifier: Apache-2.0
pragma solidity >=0.7.0 <0.9.0;

import "forge-std/Test.sol";

import {INumber} from "../test/interfaces/INumber.sol";
import {IConstructor} from "../test/interfaces/IConstructor.sol";
import {StatefulDeployer} from "./StatefulDeployer.sol";

contract StatefulDeployerTest is Test {
    StatefulDeployer public deployer;
    IConstructor public construct;

    function setUp() public {
        deployer = new StatefulDeployer();
    }

    function testSetArgs(bytes memory some) public {
        deployer.setArgs(some);
        assertEq(deployer.args(), some);
    }

    function testSetCode(string memory code) public {
        deployer.setCode(code);
        assertEq(deployer.code(), code);
    }

    function testDeployWithArgsAndCode() public {
        deployer.setArgs(
            bytes.concat(abi.encode(uint256(0x420)), abi.encode(uint256(0x420)))
        );
        deployer.setCode(
            "" "#define macro CONSTRUCTOR() = takes(0) returns (0) { \n"
            "    // Copy the first argument into memory \n"
            "    0x20                        // [size] - byte size to copy \n"
            "    0x40 codesize sub           // [offset, size] - offset in the code to copy from \n"
            "    0x00                        // [mem, offset, size] - offset in memory to copy to \n"
            "    codecopy                    // [] \n"
            "    // Store the first argument in storage \n"
            "    0x00 mload                  // [arg] \n"
            "    [CONSTRUCTOR_ARG_ONE]       // [CONSTRUCTOR_ARG_ONE, arg] \n"
            "    sstore                      // [] \n"
            "    // Copy the second argument into memory \n"
            "    0x20                        // [size] - byte size to copy \n"
            "    0x20 codesize sub           // [offset, size] - offset in the code to copy from \n"
            "    0x00                        // [mem, offset, size] - offset in memory to copy to \n"
            "    codecopy                    // [] \n"
            "    // Store the second argument in storage \n"
            "    0x00 mload                  // [arg] \n"
            "    [CONSTRUCTOR_ARG_TWO]       // [CONSTRUCTOR_ARG_TWO, arg] \n"
            "    sstore                      // [] \n" "}"
        );

        construct =
            IConstructor(deployer.deploy("test/contracts/NoConstructor"));
        assertEq(address(0x420), construct.getArgOne());
        assertEq(uint256(0x420), construct.getArgTwo());
    }
}
