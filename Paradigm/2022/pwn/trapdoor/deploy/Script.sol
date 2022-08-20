// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.16;

library console {
    address constant CONSOLE_ADDRESS = address(0x000000000000000000636F6e736F6c652e6c6f67);

    function _sendLogPayload(bytes memory payload) private view {
        uint256 payloadLength = payload.length;
        address consoleAddress = CONSOLE_ADDRESS;
        assembly {
            let payloadStart := add(payload, 32)
            let r := staticcall(gas(), consoleAddress, payloadStart, payloadLength, 0, 0)
        }
    }

    function log(string memory p0, uint256 p1, uint256 p2, uint256 p3) internal view {
        _sendLogPayload(abi.encodeWithSignature("log(string,uint,uint,uint)", p0, p1, p2, p3));
    }
}

interface FactorizorLike {
    function factorize(uint) external pure returns (uint, uint);
}

contract Deployer {
    constructor(bytes memory code) { assembly { return (add(code, 0x20), mload(code)) } }
}

contract Script {
    function run() external {
        uint expected = NUMBER;

        FactorizorLike factorizer = FactorizorLike(address(new Deployer(hex"CODE")));
        (uint a, uint b) = factorizer.factorize(expected);

        if (a > 1 && b > 1 && a != expected && b != expected && a != b && expected % a == 0 && expected % b == 0) {
            console.log("you factored the number! %d * %d = %d", a, b, expected);
        } else {
            console.log("you didn't factor the number. %d * %d != %d", a, b, expected);
        }
    }
}