// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Lib_PredeployAddresses} from "../../libraries/constants/Lib_PredeployAddresses.sol";
import {L2StandardERC20} from "./L2StandardERC20.sol";

contract L2WETH is L2StandardERC20 {
    constructor() L2StandardERC20(address(0), "Wrapped Ether", "WETH") {}
}
