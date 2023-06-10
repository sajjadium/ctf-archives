// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;

import {AppStorage} from "./libraries/LibAppStorage.sol";

import {LibDiamond} from "./libraries/LibDiamond.sol";
import {IDiamondLoupe} from "./interfaces/IDiamondLoupe.sol";
import {IDiamondCut} from "./interfaces/IDiamondCut.sol";
import {IERC173} from "./interfaces/IERC173.sol";
import {IERC165} from "./interfaces/IERC165.sol";
import {IERC20} from "./interfaces/IERC20.sol";

// It is expected that this contract is customized if you want to deploy your diamond
// with data from a deployment script. Use the init function to initialize state variables
// of your diamond. Add parameters to the init function if you need to.

contract InitDiamond {
    AppStorage internal s;

    function init(IERC20 _govToken, address _pigeonVaultFacet) external {
        LibDiamond.DiamondStorage storage ds = LibDiamond.diamondStorage();
        // adding ERC165 data
        ds.supportedInterfaces[type(IERC165).interfaceId] = true;
        ds.supportedInterfaces[type(IDiamondCut).interfaceId] = true;
        ds.supportedInterfaces[type(IDiamondLoupe).interfaceId] = true;
        ds.supportedInterfaces[type(IERC173).interfaceId] = true;

        s.proposalThreshold = 1_000_000 ether;
        s.voteThreshold = 10_000 ether;
        s.governanceToken = _govToken;
        s.pigeonVaultFacet = _pigeonVaultFacet;
    }
}
