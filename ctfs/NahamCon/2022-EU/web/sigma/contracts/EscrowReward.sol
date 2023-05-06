// SPDX-License-Identifier: Unlicensed
// @author - Ataberk Yavuzer
pragma solidity ^0.8.0;

import { ECDSA } from "./lib/ECDSA.sol";
import { HalbornToken } from "./HalbornToken.sol";
import { RewardNFT } from "./RewardNFT.sol";

contract EscrowReward {
    bool public transferHashGenerated;

    address internal immutable verifyingSigner;
    address internal immutable owner;

    RewardNFT public rewardNFT;
    HalbornToken public token;

    mapping(bytes => uint256) public nonce;

    struct TransferOperation {
        uint256 nonce;
        address sender;
        bytes4 callData;
        uint transferAmount;
        bytes signature;
    }

    using ECDSA for bytes32;

    event CallSucceed(bytes32 requestId, address indexed sender);

    modifier onlyOwner {
        require(owner == msg.sender, "EscrowReward::only owner");
        _;
    }

    constructor(address _verifyingSigner) {
        require(_verifyingSigner != address(0), "EscrowReward::zero address");
        owner = msg.sender;
        verifyingSigner = _verifyingSigner;
        token = new HalbornToken(address(this));
        rewardNFT = new RewardNFT(address(this));
    }

    function setRewardNFT(RewardNFT _rewardNft) external onlyOwner {
        require(address(_rewardNft) != address(0), "EscrowReward::zero address");
        rewardNFT = _rewardNft;
    }

    function setHalbornToken(HalbornToken _token) external onlyOwner {
        require(address(_token) != address(0), "EscrowReward::zero address");
        token = _token;
    }

    function claimNFT() external {
        require(token.balanceOf(address(this)) == 0, "EscrowReward::wrong solution");
        rewardNFT.mintAsReward(msg.sender);
    }

    function execute(TransferOperation calldata transferOp, bytes32 requestId) external returns(bool) {
        _validateSignature(transferOp, requestId);

        if(transferOp.callData == token.approve.selector) {
            (bool success, ) = address(token).call(abi.encodeWithSelector(
                transferOp.callData,
                address(this),
                transferOp.transferAmount
            ));
            require(success, "call failed");
            emit CallSucceed(requestId, transferOp.sender);
            return true;
        }

        else if (transferOp.callData == token.transferFrom.selector) {
            (bool success, ) = address(token).call(abi.encodeWithSelector(
                transferOp.callData,
                transferOp.sender,
                msg.sender,
                transferOp.transferAmount
            ));
            require(success, "call failed");
            emit CallSucceed(requestId, transferOp.sender);
            return true;
        }
        return false;
    }

    function _validateSignature(TransferOperation calldata transferOp, bytes32 requestId) internal {
        require(++nonce[transferOp.signature] == 1, "EscrowReward::signature used");
        bytes32 hash = requestId.toEthSignedMessageHash();
        require(verifyingSigner == hash.recover(transferOp.signature), "EscrowReward::wrong signature");
    }

    function getHash(TransferOperation memory transferOp) public view returns (bytes32) {
        return keccak256(abi.encode(
                transferOp.nonce,
                transferOp.sender,
                msg.sender,
                transferOp.callData,
                transferOp.transferAmount
        ));
    }

    receive() external payable {}

    fallback() external payable {}

}
