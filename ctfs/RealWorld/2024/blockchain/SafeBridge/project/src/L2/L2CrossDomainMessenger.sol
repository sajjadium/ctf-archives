// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {CrossDomainMessenger} from "../libraries/bridge/CrossDomainMessenger.sol";

contract L2CrossDomainMessenger is CrossDomainMessenger {
    constructor(address _relayer) CrossDomainMessenger(_relayer) {}
}
