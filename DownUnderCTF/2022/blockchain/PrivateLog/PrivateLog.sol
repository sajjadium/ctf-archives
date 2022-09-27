// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

/**
 * @title Private Log
 * @author Blue Alder (https://duc.tf)
 **/

import "OpenZeppelin/openzeppelin-contracts@4.3.2/contracts/proxy/utils/Initializable.sol";


contract PrivateLog is Initializable {

    bytes32 public secretHash;
    string[] public logEntries;

    constructor() {
        secretHash = 0xDEADDEADDEADDEADDEADDEADDEADDEADDEADDEADDEADDEADDEADDEADDEADDEAD;
    }

    function init(bytes32 _secretHash) payable public initializer {
        require(secretHash != 0xDEADDEADDEADDEADDEADDEADDEADDEADDEADDEADDEADDEADDEADDEADDEADDEAD);
        secretHash = _secretHash;
    }

    modifier hasSecret(string memory password, bytes32 newHash) {
        require(keccak256(abi.encodePacked(password)) == secretHash, "Incorrect Hash");
        secretHash = newHash;
        _;
    }

    function viewLog(uint256 logIndex) view public returns (string memory) {
        return logEntries[logIndex];
    } 

    function createLogEntry(string memory logEntry, string memory password, bytes32 newHash) public hasSecret(password, newHash) {
        require(bytes(logEntry).length <= 31, "log too long");   
        
        assembly {
            mstore(0x00, logEntries.slot)
            let length := sload(logEntries.slot)
            let logLength := mload(logEntry)
            sstore(add(keccak256(0x00, 0x20), length), or(mload(add(logEntry, 0x20)), mul(logLength, 2)))
            sstore(logEntries.slot, add(length, 1))
        }
    }

    function updateLogEntry(uint256 logIndex, string memory logEntry, string memory password, bytes32 newHash) public hasSecret(password, newHash) {
        require(bytes(logEntry).length <= 31, "log too long");   
        
        assembly {
            let length := mload(logEntry)
            mstore(0x00, logEntries.slot)
            sstore(add(keccak256(0x00, 0x20), logIndex), or(mload(add(logEntry, 0x20)), mul(length, 2)))
        }

    }
}