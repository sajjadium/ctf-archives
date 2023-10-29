// SPDX-License-Identifier: Apache-2.0
pragma solidity >=0.8.13 <0.9.0;

import {Vm} from "forge-std/Vm.sol";
import {strings} from "stringutils/strings.sol";
import {HuffDeployer} from "../HuffDeployer.sol";

contract StatefulDeployer {
    using strings for *;

    /// @notice Initializes cheat codes in order to use ffi to compile Huff contracts
    Vm public constant vm =
        Vm(address(bytes20(uint160(uint256(keccak256("hevm cheat code"))))));

    /// @notice additional code to append to the source file
    string public code;

    /// @notice arguments to append to the bytecode
    bytes public args;

    /// @notice sets the code to be appended to the source file
    function setCode(string memory acode) public {
        code = acode;
    }

    /// @notice sets the arguments to be appended to the bytecode
    function setArgs(bytes memory aargs) public {
        args = aargs;
    }

    /// @notice Deployment wrapper
    function deploy(string memory file) public returns (address) {
        // Split the file into it's parts
        strings.slice memory s = file.toSlice();
        strings.slice memory delim = "/".toSlice();
        string[] memory parts = new string[](s.count(delim) + 1);
        for (uint256 i = 0; i < parts.length; i++) {
            parts[i] = s.split(delim).toString();
        }

        // Re-concatenate the file with a "__TEMP__" prefix
        string memory tempFile = parts[0];
        for (uint256 i = 1; i < parts.length - 1; i++) {
            tempFile = string.concat(tempFile, "/", parts[i]);
        }
        tempFile =
            string.concat(tempFile, "/", "__TEMP__", parts[parts.length - 1]);

        // Paste the code in a new temp file
        string[] memory create_cmds = new string[](3);
        create_cmds[0] = "./scripts/file_writer.sh";
        create_cmds[1] = string.concat("src/", tempFile, ".huff");
        create_cmds[2] = string.concat(code, "\n");
        vm.ffi(create_cmds);

        // Append the real code to the temp file
        string[] memory append_cmds = new string[](3);
        append_cmds[0] = "./scripts/read_and_append.sh";
        append_cmds[1] = string.concat("src/", tempFile, ".huff");
        append_cmds[2] = string.concat("src/", file, ".huff");
        vm.ffi(append_cmds);

        // Deploy with args the temp file
        address deployed = HuffDeployer.deploy_with_args(tempFile, args);

        // Clean up temp files
        string[] memory cleanup = new string[](2);
        cleanup[0] = "rm";
        cleanup[1] = string.concat("src/", tempFile, ".huff");
        vm.ffi(cleanup);

        // Return the deployed address
        return deployed;
    }
}
