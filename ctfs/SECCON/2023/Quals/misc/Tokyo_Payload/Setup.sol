// SPDX-License-Identifier: Apache-2.0
pragma solidity 0.8.21;

import {TokyoPayload} from "./TokyoPayload.sol";

contract Setup {
    TokyoPayload public tokyoPayload;

    constructor() {
        tokyoPayload = new TokyoPayload();
    }

    function isSolved() public view returns (bool) {
        return tokyoPayload.solved();
    }
}
