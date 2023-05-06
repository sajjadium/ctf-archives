// SPDX-License-Identifier: MIT
pragma solidity ^0.8.2;

import "./interfaces/IERC20.sol";
import "./governance/Governor.sol";
import "./governance/extensions/GovernorVotes.sol";
import "./governance/extensions/GovernorCountingSimple.sol";
import "./governance/extensions/GovernorVotesQuorumFraction.sol";

contract Gov is Governor, GovernorVotes,GovernorCountingSimple,GovernorVotesQuorumFraction{
    address mytoken;
    constructor(IVotes _token)
        Governor("AAAGov")
        GovernorVotes(_token)
        GovernorVotesQuorumFraction(4)
    {
        _token.delegate(address(this));
        mytoken=address(_token);
    }

    function votingDelay() public pure override returns (uint256) {
        return 10; // 1 day
    }

    function votingPeriod() public pure override returns (uint256) {
        return 46027; // 1 week
    }

    function proposalThreshold() public pure override returns (uint256) {
        return 0;
    }
}