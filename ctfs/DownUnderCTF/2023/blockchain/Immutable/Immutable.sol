// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract Immutable {
    address public owner;
    address public contractToReview;

    error BadSubmissionSize();
    error AddressZero();

    constructor() {
        owner = msg.sender;
    }

    function submitContractForReview(address submission) external {
        if (submission == address(0)) revert AddressZero();
        uint256 size;
        assembly {
            size := extcodesize(submission)
        }
        if (size != 13) revert BadSubmissionSize();

        // Confirmed contract size - puny small lil smart contract
        contractToReview = submission;
    }

    function reviewContract() external {
        address review = contractToReview;
        if (review == address(0)) revert AddressZero();

        uint256 size;
        assembly {
            size := extcodesize(review)
        }

        // Wow big contract! How did you become so big :O
        if (size != 1337) revert BadSubmissionSize();

        contractToReview = address(0);
        owner = msg.sender;
    }
}
