// SPDX-License-Identifier: MIT

pragma solidity >=0.8.0 <0.9.0;

uint256 constant order = 0x1000000000000000000000000000000014def9dea2f79cd65812631a5cf5d3ed;
uint256 constant inf = 0x0100000000000000000000000000000000000000000000000000000000000000;
uint256 constant base = 0x5866666666666666666666666666666666666666666666666666666666666666;
uint256 constant sge = 0xecffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7f;
uint256 constant two256modOrder = 0xffffffffffffffffffffffffffffffec6ef5bf4737dcf70d6ec31748d98951d;
uint256 constant orderMinus2 = 0x1000000000000000000000000000000014def9dea2f79cd65812631a5cf5d3eb;

function pointAdd(uint256 x, uint256 y) view returns (uint256 result) {
    uint256[2] memory input = [x, y];
    bool success;
    assembly {
        success := staticcall(gas(), 21, input, 64, input, 32)
    }
    require(success);
    result = input[0];
}

function pointNeg(uint x) pure returns (uint256) {
    if (x == inf) return x;
    return x ^ uint256(0x80);
}

function pointSub(uint256 x, uint256 y) view returns (uint256 result) {
    result = pointAdd(x, pointNeg(y));
}

function scalarMult(uint256 s, uint256 p) view returns (uint256 result) {
    uint256[2] memory input = [p, s];
    bool success;
    assembly {
        success := staticcall(gas(), 22, input, 64, input, 32)
    }
    require(success);
    result = input[0];
}

function hashToPoint(bytes memory input) view returns (uint256) {
    uint256[1] memory ret = [uint256(0)];
    uint256 len = input.length;
    bool success;
    assembly {
        success := staticcall(gas(), 23, input, len, ret, 32)
    }
    require(success);
    return ret[0];
}

function hashToScalar(bytes memory message) pure returns (uint256 t) {
    uint256 s0 = uint256(keccak256(abi.encodePacked(bytes1(0xaa), message)));
    uint256 s1 = uint256(keccak256(abi.encodePacked(bytes1(0xcc), message)));
    t = addmod(mulmod(s0, two256modOrder, order), s1, order);
}

function scalarExp(uint256 b, uint256 e) view returns (uint256 result) {
    bool success;
    assembly {
        let p := mload(0x40)
        mstore(p, 0x20)
        mstore(add(p, 0x20), 0x20)
        mstore(add(p, 0x40), 0x20)
        mstore(add(p, 0x60), b)
        mstore(add(p, 0x80), e)
        mstore(add(p, 0xa0), order)
        success := staticcall(gas(), 0x05, p, 0xc0, p, 0x20)
        result := mload(p)
    }
    require(success);
}

function scalarMul(uint256 a, uint256 b) pure returns (uint256) {
    return mulmod(a, b, order);
}

function scalarAdd(uint256 a, uint256 b) pure returns (uint256) {
    return addmod(a, b, order);
}

function scalarNeg(uint256 a) pure returns (uint256) {
    if (a == 0) {
        return 0;
    }
    return order - a;
}

function scalarSub(uint256 a, uint256 b) pure returns (uint256) {
    return scalarAdd(a, scalarNeg(b));
}

function scalarInvert(uint256 t) view returns (uint256) {
    return scalarExp(t, orderMinus2);
}

function scalarDiv(uint256 a, uint256 b) view returns (uint256) {
    return scalarMul(a, scalarInvert(b));
}
