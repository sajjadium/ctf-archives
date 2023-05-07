// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ReverseMe {
    uint goal = 0x57e4e375661c72654c31645f78455d19;

    function magic1(uint x, uint n) public pure returns (uint) {
        // Something magic
        uint m = (1 << n) - 1;
        return x & m;
    }

    function magic2(uint x) public pure returns (uint) {
        // Something else magic
        uint i = 0;
        while ((x >>= 1) > 0) {
            i += 1;
        }
        return i;
    }

    function checkflag(bytes16 flag, bytes16 y) public view returns (bool) {
        return (uint128(flag) ^ uint128(y) == goal);
    }

    modifier checker(bytes16 key) {
        require(bytes8(key) == 0x3492800100670155, "Wrong key!");
        require(uint64(uint128(key)) == uint32(uint128(key)), "Wrong key!");
        require(magic1(uint128(key), 16) == 0x1964, "Wrong key!");
        require(magic2(uint64(uint128(key))) == 16, "Wrong key!");
        _;
    }

    function unlock(bytes16 key, bytes16 flag) public view checker(key) {
        // Main function
        require(checkflag(flag, key), "Flag is wrong!");
    }
}