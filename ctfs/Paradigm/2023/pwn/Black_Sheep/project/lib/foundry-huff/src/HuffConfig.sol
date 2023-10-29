// SPDX-License-Identifier: Apache-2.0
pragma solidity >=0.8.13 <0.9.0;

import {Vm} from "forge-std/Vm.sol";
import {strings} from "stringutils/strings.sol";

contract HuffConfig {
    using strings for *;

    /// @notice Initializes cheat codes in order to use ffi to compile Huff contracts
    Vm public constant vm = Vm(address(bytes20(uint160(uint256(keccak256("hevm cheat code"))))));

    /// @notice Struct that represents a constant to be passed to the `-c` flag
    struct Constant {
        string key;
        string value;
    }

    /// @notice additional code to append to the source file
    string public code;

    /// @notice arguments to append to the bytecode
    bytes public args;

    /// @notice value to deploy the contract with
    uint256 public value;

    /// @notice whether to broadcast the deployment tx
    bool public should_broadcast;

    /// @notice constant overrides for the current compilation environment
    Constant[] public const_overrides;

    /// @notice sets the code to be appended to the source file
    function with_code(string memory code_) public returns (HuffConfig) {
        code = code_;
        return this;
    }

    /// @notice sets the arguments to be appended to the bytecode
    function with_args(bytes memory args_) public returns (HuffConfig) {
        args = args_;
        return this;
    }

    /// @notice sets the amount of wei to deploy the contract with
    function with_value(uint256 value_) public returns (HuffConfig) {
        value = value_;
        return this;
    }

    /// @notice sets a constant to a bytes memory value in the current compilation environment
    /// @dev The `value` string must contain a valid hex number that is <= 32 bytes
    ///      i.e. "0x01", "0xa57b", "0x0de0b6b3a7640000", etc. 
    function with_constant(
        string memory key,
        string memory value_
    ) public returns (HuffConfig) {
        const_overrides.push(Constant(key, value_));
        return this;
    }

    /// @notice sets a constant to an address value in the current compilation environment
    function with_addr_constant(
        string memory key,
        address value_
    ) public returns (HuffConfig) {
        const_overrides.push(Constant(key, bytesToString(abi.encodePacked(value_))));
        return this;
    }

    /// @notice sets a constant to a bytes32 value in the current compilation environment
    function with_bytes32_constant(
        string memory key,
        bytes32 value_
    ) public returns (HuffConfig) {
        const_overrides.push(Constant(key, bytesToString(abi.encodePacked(value_))));
        return this;
    }

    /// @notice sets a constant to a uint256 value in the current compilation environment
    function with_uint_constant(
        string memory key,
        uint256 value_
    ) public returns (HuffConfig) {
        const_overrides.push(Constant(key, bytesToString(abi.encodePacked(value_))));
        return this;
    }

    /// @notice sets whether to broadcast the deployment
    function set_broadcast(bool broadcast) public returns (HuffConfig) {
        should_broadcast = broadcast;
        return this;
    }

    /// @notice Checks for huffc binary conflicts
    function binary_check() public {
        string[] memory bincheck = new string[](1);
        bincheck[0] = "./lib/foundry-huff/scripts/binary_check.sh";
        bytes memory retData = vm.ffi(bincheck);
        bytes8 first_bytes = retData[0];
        bool decoded = first_bytes == bytes8(hex"01");
        require(
            decoded,
            "Invalid huffc binary. Run `curl -L get.huff.sh | bash` and `huffup` to fix."
        );
    }

    function bytes32ToString(bytes32 x) internal pure returns (string memory) {
        string memory result;
        for (uint256 j = 0; j < x.length; j++) {
            result = string.concat(
                result, string(abi.encodePacked(uint8(x[j]) % 26 + 97))
            );
        }
        return result;
    }

    function bytesToString(bytes memory data) public pure returns(string memory) {
        bytes memory alphabet = "0123456789abcdef";

        bytes memory str = new bytes(2 + data.length * 2);
        str[0] = "0";
        str[1] = "x";
        for (uint i = 0; i < data.length; i++) {
            str[2+i*2] = alphabet[uint(uint8(data[i] >> 4))];
            str[3+i*2] = alphabet[uint(uint8(data[i] & 0x0f))];
        }
        return string(str);
    }

    /// @notice Deploy the Contract
    function deploy(string memory file) public payable returns (address) {
        binary_check();

        // Split the file into it's parts
        strings.slice memory s = file.toSlice();
        strings.slice memory delim = "/".toSlice();
        string[] memory parts = new string[](s.count(delim) + 1);
        for (uint256 i = 0; i < parts.length; i++) {
            parts[i] = s.split(delim).toString();
        }

        // Get the system time with our script
        string[] memory time = new string[](1);
        time[0] = "./lib/foundry-huff/scripts/rand_bytes.sh";
        bytes memory retData = vm.ffi(time);
        string memory rand_bytes =
            bytes32ToString(keccak256(abi.encode(bytes32(retData))));

        // Re-concatenate the file with a "__TEMP__" prefix
        string memory tempFile = parts[0];
        if (parts.length <= 1) {
            tempFile = string.concat("__TEMP__", rand_bytes, tempFile);
        } else {
            for (uint256 i = 1; i < parts.length - 1; i++) {
                tempFile = string.concat(tempFile, "/", parts[i]);
            }
            tempFile = string.concat(
                tempFile, "/", "__TEMP__", rand_bytes, parts[parts.length - 1]
            );
        }

        // Paste the code in a new temp file
        string[] memory create_cmds = new string[](3);
        // TODO: create_cmds[0] = "$(find . -name \"file_writer.sh\")";
        create_cmds[0] = "./lib/foundry-huff/scripts/file_writer.sh";
        create_cmds[1] = string.concat("src/", tempFile, ".huff");
        create_cmds[2] = string.concat(code, "\n");
        vm.ffi(create_cmds);

        // Append the real code to the temp file
        string[] memory append_cmds = new string[](3);
        append_cmds[0] = "./lib/foundry-huff/scripts/read_and_append.sh";
        append_cmds[1] = string.concat("src/", tempFile, ".huff");
        append_cmds[2] = string.concat("src/", file, ".huff");
        vm.ffi(append_cmds);

        /// Create a list of strings with the commands necessary to compile Huff contracts
        string[] memory cmds = new string[](3);
        if (const_overrides.length > 0) {
            cmds = new string[](4 + const_overrides.length);
            cmds[3] = "-c";

            Constant memory cur_const;
            for (uint256 i; i < const_overrides.length; i++) {
                cur_const = const_overrides[i];
                cmds[4 + i] = string.concat(cur_const.key, "=", cur_const.value);
            }
        }

        cmds[0] = "huffc";
        cmds[1] = string(string.concat("src/", tempFile, ".huff"));
        cmds[2] = "-b";

        /// @notice compile the Huff contract and return the bytecode
        bytes memory bytecode = vm.ffi(cmds);
        bytes memory concatenated = bytes.concat(bytecode, args);

        // Clean up temp files
        string[] memory cleanup = new string[](2);
        cleanup[0] = "rm";
        cleanup[1] = string.concat("src/", tempFile, ".huff");
        vm.ffi(cleanup);

        /// @notice deploy the bytecode with the create instruction
        address deployedAddress;
        if (should_broadcast) vm.broadcast();
        assembly {
            let val := sload(value.slot)
            deployedAddress := create(val, add(concatenated, 0x20), mload(concatenated))
        }

        /// @notice check that the deployment was successful
        require(
            deployedAddress != address(0), "HuffDeployer could not deploy contract"
        );

        /// @notice return the address that the contract was deployed to
        return deployedAddress;
    }
}
