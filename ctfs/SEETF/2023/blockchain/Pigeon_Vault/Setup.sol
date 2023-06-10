// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;

import {IDiamondCut} from "./interfaces/IDiamondCut.sol";
import {IDiamondLoupe} from "./interfaces/IDiamondLoupe.sol";
import {IOwnershipFacet} from "./interfaces/IOwnershipFacet.sol";
import {IERC20} from "./interfaces/IERC20.sol";

import {DiamondCutFacet} from "./facets/DiamondCutFacet.sol";
import {OwnershipFacet} from "./facets/OwnershipFacet.sol";
import {DiamondLoupeFacet} from "./facets/DiamondLoupeFacet.sol";
import {FeatherCoinFacet} from "./facets/FTCFacet.sol";
import {DAOFacet} from "./facets/DAOFacet.sol";
import {PigeonVaultFacet} from "./facets/PigeonVaultFacet.sol";

import {PigeonDiamond} from "./PigeonDiamond.sol";
import {InitDiamond} from "./InitDiamond.sol";

contract Setup {
    DiamondCutFacet public diamondCutFacet;
    OwnershipFacet public ownershipFacet;
    DiamondLoupeFacet public diamondLoupeFacet;
    FeatherCoinFacet public ftcFacet;
    DAOFacet public daoFacet;
    PigeonVaultFacet public pigeonVaultFacet;

    PigeonDiamond public pigeonDiamond;
    InitDiamond public initDiamond;

    bool public claimed;

    constructor() payable {
        diamondCutFacet = new DiamondCutFacet();
        ownershipFacet = new OwnershipFacet();
        diamondLoupeFacet = new DiamondLoupeFacet();
        ftcFacet = new FeatherCoinFacet();
        daoFacet = new DAOFacet();
        pigeonVaultFacet = new PigeonVaultFacet();

        pigeonDiamond = new PigeonDiamond(address(this), address(diamondCutFacet));
        initDiamond = new InitDiamond();

        IDiamondCut.FacetCut[] memory diamondCut = new IDiamondCut.FacetCut[](5);

        // Setup DiamondLoupeFacet
        bytes4[] memory diamondLoupeSelectors = new bytes4[](5);
        diamondLoupeSelectors[0] = bytes4(hex"cdffacc6");
        diamondLoupeSelectors[1] = bytes4(hex"52ef6b2c");
        diamondLoupeSelectors[2] = bytes4(hex"adfca15e");
        diamondLoupeSelectors[3] = bytes4(hex"7a0ed627");
        diamondLoupeSelectors[4] = bytes4(hex"01ffc9a7");

        diamondCut[0] = IDiamondCut.FacetCut({
            facetAddress: address(diamondLoupeFacet),
            action: IDiamondCut.FacetCutAction.Add,
            functionSelectors: diamondLoupeSelectors
        });

        // Setup OwnershipFacet
        bytes4[] memory ownershipFacetSelectors = new bytes4[](2);
        ownershipFacetSelectors[0] = bytes4(hex"8da5cb5b");
        ownershipFacetSelectors[1] = bytes4(hex"f2fde38b");

        diamondCut[1] = IDiamondCut.FacetCut({
            facetAddress: address(ownershipFacet),
            action: IDiamondCut.FacetCutAction.Add,
            functionSelectors: ownershipFacetSelectors
        });

        // Setup FTCFacet
        bytes4[] memory ftcFacetSelectors = new bytes4[](15);
        ftcFacetSelectors[0] = bytes4(hex"dd62ed3e");
        ftcFacetSelectors[1] = bytes4(hex"095ea7b3");
        ftcFacetSelectors[2] = bytes4(hex"70a08231");
        ftcFacetSelectors[3] = bytes4(hex"313ce567");
        ftcFacetSelectors[4] = bytes4(hex"5c19a95c");
        ftcFacetSelectors[5] = bytes4(hex"34940fa8");
        ftcFacetSelectors[6] = bytes4(hex"b4b5ea57");
        ftcFacetSelectors[7] = bytes4(hex"42061268");
        ftcFacetSelectors[8] = bytes4(hex"782d6fe1");
        ftcFacetSelectors[9] = bytes4(hex"40c10f19");
        ftcFacetSelectors[10] = bytes4(hex"06fdde03");
        ftcFacetSelectors[11] = bytes4(hex"95d89b41");
        ftcFacetSelectors[12] = bytes4(hex"18160ddd");
        ftcFacetSelectors[13] = bytes4(hex"a9059cbb");
        ftcFacetSelectors[14] = bytes4(hex"23b872dd");

        diamondCut[2] = IDiamondCut.FacetCut({
            facetAddress: address(ftcFacet),
            action: IDiamondCut.FacetCutAction.Add,
            functionSelectors: ftcFacetSelectors
        });

        // Setup DAOFacet
        bytes4[] memory daoFacetSelectors = new bytes4[](4);
        daoFacetSelectors[0] = bytes4(hex"aad6756f");
        daoFacetSelectors[1] = bytes4(hex"0d61b519");
        daoFacetSelectors[2] = bytes4(hex"ece40cc1");
        daoFacetSelectors[3] = bytes4(hex"abdc14c5");

        diamondCut[3] = IDiamondCut.FacetCut({
            facetAddress: address(daoFacet),
            action: IDiamondCut.FacetCutAction.Add,
            functionSelectors: daoFacetSelectors
        });

        // Setup PigeonVaultFacet
        bytes4[] memory pigeonVaultFacetSelectors = new bytes4[](3);
        pigeonVaultFacetSelectors[0] = bytes4(hex"8b7afe2e");
        pigeonVaultFacetSelectors[1] = bytes4(hex"db2e21bc");
        pigeonVaultFacetSelectors[2] = bytes4(hex"32a2c5d0");

        diamondCut[4] = IDiamondCut.FacetCut({
            facetAddress: address(pigeonVaultFacet),
            action: IDiamondCut.FacetCutAction.Add,
            functionSelectors: pigeonVaultFacetSelectors
        });

        bytes memory init =
            abi.encodeWithSelector(InitDiamond.init.selector, IERC20(address(ftcFacet)), address(pigeonVaultFacet));

        IDiamondCut(address(pigeonDiamond)).diamondCut(diamondCut, address(initDiamond), init);

        IERC20(address(pigeonDiamond)).mint(address(this), 1_000_000 ether);

        (bool success,) = payable(address(pigeonDiamond)).call{value: msg.value}("");
        require(success, "ETH failed to send");

        // Ensure everything is setup correctly
        address[] memory facetAddresses = IDiamondLoupe(address(pigeonDiamond)).facetAddresses();
        assert(facetAddresses.length == 6);

        assert(address(pigeonDiamond).balance == msg.value);
        assert(IERC20(address(pigeonDiamond)).balanceOf(address(this)) == 1_000_000 ether);
    }

    function claim() external {
        require(!claimed, "You already claimed");

        bool success = IERC20(address(pigeonDiamond)).transfer(msg.sender, 10_000 ether);
        require(success, "Failed to send");
    }

    function isSolved() external view returns (bool) {
        return (IOwnershipFacet(address(pigeonDiamond)).owner() == msg.sender && msg.sender.balance >= 3000 ether);
    }
}
