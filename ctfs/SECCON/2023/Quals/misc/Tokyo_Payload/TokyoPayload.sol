// SPDX-License-Identifier: Apache-2.0
pragma solidity 0.8.21;

contract TokyoPayload {
    bool public solved;
    uint256 public gasLimit;

    function tokyoPayload(uint256 x, uint256 y) public {
        require(x >= 0x40);
        resetGasLimit();
        assembly {
            calldatacopy(x, 0, calldatasize())
        }
        function()[] memory funcs;
        uint256 z = y;
        funcs[z]();
    }

    function load(uint256 i) public pure returns (uint256 a, uint256 b, uint256 c) {
        assembly {
            a := calldataload(i)
            b := calldataload(add(i, 0x20))
            c := calldataload(add(i, 0x40))
        }
    }

    function createArray(uint256 length) public pure returns (uint256[] memory) {
        return new uint256[](length);
    }

    function resetGasLimit() public {
        uint256[] memory arr;
        gasLimit = arr.length;
    }

    function delegatecall(address addr) public {
        require(msg.sender == address(0xCAFE));
        (bool success,) = addr.delegatecall{gas: gasLimit & 0xFFFF}("");
        require(success);
    }
}
