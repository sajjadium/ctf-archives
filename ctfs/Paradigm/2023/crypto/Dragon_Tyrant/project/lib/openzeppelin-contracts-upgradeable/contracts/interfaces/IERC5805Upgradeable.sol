// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v4.9.0) (interfaces/IERC5805.sol)

pragma solidity ^0.8.19;

import { IVotesUpgradeable } from "../governance/utils/IVotesUpgradeable.sol";
import { IERC6372Upgradeable } from "./IERC6372Upgradeable.sol";

interface IERC5805Upgradeable is IERC6372Upgradeable, IVotesUpgradeable {}
