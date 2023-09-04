// SPDX-License-Identifier: MIT
pragma solidity 0.8.19;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/interfaces/IERC20.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";
import { ud, convert } from "@prb/math/UD60x18.sol";

import "./FreqBand.sol";
import "./SampleEditor.sol";
import "./Equalizer.sol";

contract MusicRemixer {

    uint constant private INITIAL_VOLUME = 100 ether;
    address constant private SIGNER = 0x886A1C4798d270902E490b488C4431F8870bCDE3;

    SampleEditor public sampleEditor;
    Equalizer public equalizer;

    mapping(bytes => bool) public usedRedemptionCode;

    event FlagCaptured();

    error TooEasy(uint256 level);
    error CodeRedeemed();
    error InvalidCode();

    constructor() payable {
        sampleEditor = new SampleEditor();

        address[3] memory bands;
        bands[0] = address(0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE); // XDddddDdddDdDdd
        bands[1] = address(new FreqBand("Instrument", "INST"));
        bands[2] = address(new FreqBand("Vocal", "VOCAL"));

        FreqBand(bands[1]).mint(address(this), INITIAL_VOLUME);
        FreqBand(bands[2]).mint(address(this), INITIAL_VOLUME);

        equalizer = new Equalizer(bands);

        uint[3] memory amounts = [INITIAL_VOLUME, INITIAL_VOLUME, INITIAL_VOLUME];
        IERC20(bands[1]).approve(address(equalizer), amounts[1]);
        IERC20(bands[2]).approve(address(equalizer), amounts[2]);
        equalizer.increaseVolume{value: 100 ether}(amounts);

        uint8 v = 28;
        bytes32 r = hex"1337C0DEC0DEC0DEC0DEC0DEC0DEC0DEC0DEC0DEC0DEC0DEC0DEC0DEC0DE1337";
        bytes32 s = hex"1337C0DEC0DEC0DEC0DEC0DEC0DEC0DEC0DEC0DEC0DEC0DEC0DEC0DEC0DE1337";
        usedRedemptionCode[abi.encodePacked(r, s, v)] = true;
    }

    function getMaterial(bytes memory redemptionCode) external {
        if (usedRedemptionCode[redemptionCode])
            revert CodeRedeemed();
        bytes32 hash = ECDSA.toEthSignedMessageHash(abi.encodePacked("Music Remixer Pro Material"));
        if (ECDSA.recover(hash, redemptionCode) != SIGNER)
            revert InvalidCode();
        
        usedRedemptionCode[redemptionCode] = true;

        FreqBand(equalizer.bands(1)).mint(msg.sender, 1 ether);
        FreqBand(equalizer.bands(2)).mint(msg.sender, 1 ether);
    }

    function _getComplexity(uint256 n) internal pure returns (uint256 c) {
        bytes memory s = bytes(Strings.toString(n));
        bool[] memory v = new bool[](10);
        for (uint i; i < s.length; ++i) {
            v[uint8(s[i]) - 48] = true;
        }
        for (uint i; i < 10; ++i) {
            if (v[i]) ++c;
        }
    }

    function getSongLevel() public view returns (uint256) {
        return convert(ud(sampleEditor.region_tempo() * 1e18).log2()) * _getComplexity(equalizer.getGlobalInfo());  // log2(tempo) * complexity
    }

    function finish() external {
        uint256 level = getSongLevel();
        if (level < 30)
            revert TooEasy(level);
        emit FlagCaptured();
    }
}
