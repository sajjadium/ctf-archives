// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ICrossDomainMessenger} from "./ICrossDomainMessenger.sol";

contract CrossDomainMessenger is ICrossDomainMessenger {
    address public relayer;
    uint256 public messageNonce;

    mapping(bytes32 => bool) public relayedMessages;
    mapping(bytes32 => bool) public successfulMessages;
    mapping(bytes32 => bool) public sentMessages;

    address internal xDomainMsgSender = 0x000000000000000000000000000000000000dEaD;
    address internal constant DEFAULT_XDOMAIN_SENDER = 0x000000000000000000000000000000000000dEaD;

    constructor(address _relayer) {
        relayer = _relayer;
    }

    modifier onlyRelayer() {
        require(msg.sender == relayer, "not relayer");
        _;
    }

    function xDomainMessageSender() public view returns (address) {
        require(xDomainMsgSender != DEFAULT_XDOMAIN_SENDER, "xDomainMessageSender is not set");
        return xDomainMsgSender;
    }

    /**
     * Sends a cross domain message to the target messenger.
     * @param _target Target contract address.
     * @param _message Message to send to the target.
     */
    function sendMessage(address _target, bytes memory _message) public {
        bytes memory xDomainCalldata = encodeXDomainCalldata(_target, msg.sender, _message, messageNonce);

        sentMessages[keccak256(xDomainCalldata)] = true;

        emit SentMessage(_target, msg.sender, _message, messageNonce);
        messageNonce += 1;
    }

    /**
     * Relays a cross domain message to a contract.
     * @param _target Target contract address.
     * @param _sender Message sender address.
     * @param _message Message to send to the target.
     * @param _messageNonce Nonce for the provided message.
     */
    function relayMessage(address _target, address _sender, bytes memory _message, uint256 _messageNonce)
        public
        onlyRelayer
    {
        // anti reentrance
        require(xDomainMsgSender == DEFAULT_XDOMAIN_SENDER, "already in execution");

        bytes memory xDomainCalldata = encodeXDomainCalldata(_target, _sender, _message, _messageNonce);

        bytes32 xDomainCalldataHash = keccak256(xDomainCalldata);

        require(successfulMessages[xDomainCalldataHash] == false, "Provided message has already been received.");

        xDomainMsgSender = _sender;
        (bool success,) = _target.call(_message);
        xDomainMsgSender = DEFAULT_XDOMAIN_SENDER;

        // Mark the message as received if the call was successful. Ensures that a message can be
        // relayed multiple times in the case that the call reverted.
        if (success == true) {
            successfulMessages[xDomainCalldataHash] = true;
            emit RelayedMessage(xDomainCalldataHash);
        } else {
            emit FailedRelayedMessage(xDomainCalldataHash);
        }
    }

    /**
     * Generates the correct cross domain calldata for a message.
     * @param _target Target contract address.
     * @param _sender Message sender address.
     * @param _message Message to send to the target.
     * @param _messageNonce Nonce for the provided message.
     * @return ABI encoded cross domain calldata.
     */
    function encodeXDomainCalldata(address _target, address _sender, bytes memory _message, uint256 _messageNonce)
        internal
        pure
        returns (bytes memory)
    {
        return abi.encodeWithSignature(
            "relayMessage(address,address,bytes,uint256)", _target, _sender, _message, _messageNonce
        );
    }
}
