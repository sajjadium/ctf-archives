// SPDX-License-Identifier: MIT
pragma solidity 0.8.30;

import {BlockJail} from "./BlockJail.sol";
import {PalaceVault} from "./PalaceVault.sol";

contract Setup {
    error BadPrediction();
    error MissingFunds();

    BlockJail public TARGET;
    address payable public PALACE;

    constructor() payable {
        if (msg.value == 0) revert MissingFunds();

        address predictedTarget = _createAddress(address(this), 2);
        uint256 palaceFunds = msg.value / 2;
        PalaceVault palace = new PalaceVault{value: palaceFunds}(predictedTarget);
        PALACE = payable(address(palace));
        TARGET = new BlockJail{value: msg.value - palaceFunds}(PALACE);

        if (address(TARGET) != predictedTarget) revert BadPrediction();
    }

    function isSolved() external view returns (bool) {
        return TARGET.pathOpened() && address(TARGET).balance == 0
            && PalaceVault(PALACE).isSolved();
    }

    function _createAddress(address deployer, uint8 nonce) private pure returns (address) {
        return address(
            uint160(
                uint256(
                    keccak256(
                        abi.encodePacked(
                            bytes1(0xd6), bytes1(0x94), deployer, bytes1(nonce)
                        )
                    )
                )
            )
        );
    }
}
