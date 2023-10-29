pragma solidity ^0.8.20;

abstract contract IBridge {
    mapping(address => uint256) public remoteBridgeChainId;
    uint256 public relayedMessageSenderChainId;
    address public relayedMessageSenderAddress;
}
