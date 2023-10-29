// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.19;

import "./OwnedUpgradeable.sol";
import "./Interfaces.sol";

contract Randomness is IRandomness {
    error AlreadySet();
    // https://eips.ethereum.org/EIPS/eip-197 Y^2 = X^3 + 3
    // a generator of alt_bn128 (bn254)

    uint256 public constant Gx = 1;
    uint256 public constant Gy = 2;
    uint256 public immutable Px;
    uint256 public immutable Py;
    uint256 public immutable Qx;
    uint256 public immutable Qy;
    uint256 public constant fieldOrder =
        uint256(21888242871839275222246405745257275088696311157297823662689037894645226208583);
    uint256 public constant groupOrder =
        uint256(21888242871839275222246405745257275088548364400416034343698204186575808495617);

    constructor() {
        uint256 P_x;
        uint256 P_y;
        uint256 Q_x;
        uint256 Q_y;

        bytes32 r = bytes32(uint256(0x123456789));

        assembly {
            mstore(0x80, Gx)
            mstore(0xa0, Gy)
            mstore(0xc0, r)
            if iszero(staticcall(gas(), 0x07, 0x80, 0x60, 0x80, 0x40)) { revert(0, 0) }
            P_x := mload(0x80)
            P_y := mload(0xa0)

            mstore(0x80, Gx)
            mstore(0xa0, Gy)
            mstore(0xc0, r)
            mstore(0xc0, keccak256(0xc0, 0x20))
            if iszero(staticcall(gas(), 0x07, 0x80, 0x60, 0x80, 0x40)) { revert(0, 0) }
            Q_x := mload(0x80)
            Q_y := mload(0xa0)
        }

        Px = P_x;
        Py = P_y;
        Qx = Q_x;
        Qy = Q_y;
    }

    /// @notice Generates a sequence of random numbers from an initial seed
    /// @param seed The initial seed
    /// @param rounds The round to generate
    /// @return rand The generated randomness for the round
    function generate(bytes32 seed, uint256 rounds) external view override returns (bytes32 rand) {
        uint256 Q_x = Qx;
        uint256 Q_y = Qy;
        uint256 P_x = Px;
        uint256 P_y = Py;
        assembly {
            mstore(0x00, P_x)
            mstore(0x20, P_y)
            mstore(0x40, seed)
            for { let i := 0 } lt(i, rounds) { i := add(i, 1) } {
                if iszero(staticcall(gas(), 0x07, 0x00, 0x60, 0x40, 0x40)) { revert(0, 0) }
            }
            mstore(0x00, Q_x)
            mstore(0x20, Q_y)
            if iszero(staticcall(gas(), 0x07, 0x00, 0x60, 0x40, 0x40)) { revert(0, 0) }
            rand := mload(0x40)
            mstore(0x40, 0x80)
        }
    }
}
