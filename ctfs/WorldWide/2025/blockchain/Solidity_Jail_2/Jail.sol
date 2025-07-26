// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BytecodeRunner {

    string public flag = "wwf{REDACTED}";

    function run(bytes memory _bytecode, bytes32 _salt) public
    returns (bool success, bytes memory result)
    {
        address newContract;
        assembly {
            newContract := create2(
                0,
                add(_bytecode, 0x20),
                mload(_bytecode),
                _salt
            )
            if iszero(newContract) {
                revert(0, 0)
            }
        }

        bytes memory callData = abi.encodeWithSelector(
            bytes4(keccak256("main()"))
        );

        (success, result) = newContract.call(callData);
        require(success, "Execution of main() failed.");
    }
}
