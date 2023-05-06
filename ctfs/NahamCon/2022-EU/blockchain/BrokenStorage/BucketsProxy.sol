
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";
import "./Buckets.sol";

contract BucketsProxy is ERC1967Proxy {
    // a secret to change the proxy admin in case of an emergency
    // e. g. if the original admin dies
    uint256 public salt;

    constructor(address logic, uint256 premint) ERC1967Proxy(logic, abi.encodeWithSelector(Buckets.initialize.selector, premint)) {
        _changeAdmin(msg.sender);
    }

    // a failsafe admin has a secret address derived from the 256bit secret
    // we allow the method to be called by anyone to not to reveal secret failsafe addresses
    function setFailsafeAdmin(uint256 salt_) external {
        require(salt_ != 0, "SALT_CANNOT_BE_ZERO");
        salt = salt_;
    }

    // only the address that matches the secret should be able to run this method
    // this method should be called in emergency cases when the original administrator has disappeared
    function changeAdmin() external {
        require(keccak256(abi.encode(salt, msg.sender)) == keccak256(abi.encode(_getAdmin())));
        _changeAdmin(msg.sender);
    }

    // upgrade the Buckets implementation
    function upgradeTo(address newImplementation) external {
        require(_getAdmin() == msg.sender, "ADMIN_ONLY");
        _upgradeTo(newImplementation);
    }

    function getAdmin() external view returns(address){
        return _getAdmin();
    }
    
}