// SPDX-License-Identifier: MIT

pragma solidity >=0.8.0 <0.9.0;

import * as ed from "./ed25519.sol";
import * as bn from "./bn256.sol";

uint256 constant bits = 4;

struct dleqProof {
    uint256[bits] CG;
    uint256[bits] CH;
    uint256[bits] eG;
    uint256[bits] eH;
    uint256[bits] a0;
    uint256[bits] a1;
    uint256[bits] b0;
    uint256[bits] b1;
}

contract Game {
    string public hint = "DLEQ Across ed25519 and bn256";
    bool public isSolved = false;
    bool challgenGenerated = false;
    uint256 public G2 = 0;
    uint256 public H2 = 0;
    uint256 public xG2 = 0;
    uint256 constant xLimit = 2**bits;

    function newChallenge() public returns (uint256) {
        require(!challgenGenerated);
        uint256 x = ed.hashToScalar(
            abi.encodePacked(address(this), block.difficulty, block.coinbase, block.timestamp, block.number, block.gaslimit)
        ) % xLimit;
        G2 = ed.hashToPoint(
            abi.encodePacked(address(this), block.difficulty, block.coinbase, block.timestamp, block.number, block.gaslimit)
        );
        H2 = bn.hashToPoint(
            abi.encodePacked(address(this), block.difficulty, block.coinbase, block.timestamp, block.number, block.gaslimit)
        );
        xG2 = ed.scalarMult(x, G2);
        challgenGenerated = true;
        return x;
    }

    function check(uint256 xH2, dleqProof calldata proof) public {
        uint len;
        assembly { len := extcodesize(caller()) }
        require(len != 0);
        require(challgenGenerated);
        {
            uint256 cur = 1;
            uint256 Gsum = ed.inf;
            uint256 Hsum = bn.inf;
            for (uint i = 0; i < bits; i++) {
                Gsum = ed.pointAdd(Gsum, ed.scalarMult(cur, proof.CG[i]));
                Hsum = bn.pointAdd(Hsum, bn.scalarMult(cur, proof.CH[i]));
                cur *= 2;
            }
            require(Gsum == xG2);
            require(Hsum == xH2);
        }
        for (uint i = 0; i < bits; i++) {
            bytes memory bts = abi.encode(
                proof.CG[i], proof.CH[i], 
                ed.pointSub(
                    ed.scalarMult(proof.a1[i], ed.base),
                    ed.scalarMult(proof.eG[i], proof.CG[i])
                ), 
                bn.pointSub(
                    bn.scalarMult(proof.b1[i], bn.base),
                    bn.scalarMult(proof.eH[i], proof.CH[i])
                )
            );
            uint256 e1G = ed.hashToScalar(bts);
            uint256 e1H = bn.hashToScalar(bts);
            bts = abi.encode(
                proof.CG[i], proof.CH[i],
                ed.pointSub(
                    ed.scalarMult(proof.a0[i], ed.base),
                    ed.scalarMult(e1G, ed.pointSub(proof.CG[i], G2))
                ),
                bn.pointSub(
                    bn.scalarMult(proof.b0[i], bn.base),
                    bn.scalarMult(e1H, bn.pointSub(proof.CH[i], H2))
                )
            );
            require(proof.eG[i] == ed.hashToScalar(bts));
            require(proof.eH[i] == bn.hashToScalar(bts));
        }
        isSolved = true;
    }
}