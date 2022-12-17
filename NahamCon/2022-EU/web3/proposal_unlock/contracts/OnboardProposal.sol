// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.8.13;

interface SimpleIERC20 {
    function totalSupply() external view returns (uint256);

    function balanceOf(address account) external view returns (uint256);

    function transfer(address to, uint256 amount) external returns (bool);

    function transferFrom(
        address from,
        address to,
        uint256 amount
    ) external returns (bool);
}

interface IHalbornToken is SimpleIERC20 {
    // Allows minting enought HAL for a proposal
    function mint() external;

    // Burn Halborn token
    function burnHalborn(address _account, uint256 _amount) external;

    function setOnboardProposal(address _new) external;
}

interface IVeHAL is SimpleIERC20 {
    // We give a 10% of the initial supply to the first caller!
    function airdrop() external;

    // Get the locked amount of a user's veDeg
    function locked(address _user) external view returns (uint256);

    // Lock veHAL
    function lockVeHAL(address _to, uint256 _amount) external;

    // Unlock veHAL
    function unlockVeHAL(address _to, uint256 _amount) external;

    function setOnboardProposal(address _new) external;
}

/**
 * @notice Onboard Proposal
 */
contract OnboardProposal {

    address owner;
    IHalbornToken internal deg;
    IVeHAL internal veDeg;

    modifier onlyOwner() {
        require(msg.sender == owner, "Not the owner");
        _;
    }

    uint256 public constant PROPOSAL_VOTING_PERIOD = 18 hours;

    // HAL threshold for starting a report
    uint256 public constant PROPOSE_THRESHOLD = 10000 ether;

    // 10000 = 100%
    uint256 public constant MAX_CAPACITY_RATIO = 10000;

    // Status parameters for a voting
    uint256 internal constant INIT_STATUS = 0;
    uint256 internal constant PENDING_STATUS = 1;
    uint256 internal constant VOTING_STATUS = 2;
    uint256 internal constant SETTLED_STATUS = 3;

    // Result parameters for a voting
    uint256 internal constant INIT_RESULT = 0;
    uint256 internal constant PASS_RESULT = 1;
    uint256 internal constant REJECT_RESULT = 2;
    uint256 internal constant TIED_RESULT = 3;
    uint256 internal constant FAILED_RESULT = 4;

    // Voting choices
    uint256 internal constant VOTE_FOR = 1;
    uint256 internal constant VOTE_AGAINST = 2;


    event NewProposal(
        string name,
        address token,
        address proposer,
        uint256 priceRatio
    );

    event ProposalVoted(
        uint256 proposalId,
        address indexed user,
        uint256 voteFor,
        uint256 amount
    );

    event ProposalSettled(uint256 proposalId, uint256 result);

    event ProposalFailed(uint256 proposalId);

    event Claimed(uint256 proposalId, address user, uint256 amount);

    // ---------------------------------------------------------------------------------------- //
    // *************************************** Errors ***************************************** //
    // ---------------------------------------------------------------------------------------- //

    error OnboardProposal__WrongStatus();
    error OnboardProposal__WrongChoice();
    error OnboardProposal__ChooseBothSides();
    error OnboardProposal__NotEnoughVeHAL();
    error OnboardProposal__NotSettled();
    error OnboardProposal__NotWrongChoice();
    error OnboardProposal__ProposeNotExist();
    error OnboardProposal__AlreadyProtected();
    error OnboardProposal__WrongCapacity();
    error OnboardProposal__WrongPremium();
    error OnboardProposal__ZeroAmount();

    // ---------------------------------------------------------------------------------------- //
    // ************************************* Variables **************************************** //
    // ---------------------------------------------------------------------------------------- //

    // Total number of reports
    uint256 public proposalCounter;

    // Proposal quorum ratio
    uint256 public quorumRatio;

    struct Proposal {
        string name; // Pool name ("JOE", "GMX")
        address protocolToken; // Protocol native token address
        address proposer; // Proposer address
        uint256 proposeTimestamp; // Timestamp when proposing
        uint256 numFor; // Votes voting for
        uint256 numAgainst; // Votes voting against
        uint256 status; // Current status (PENDING, VOTING, SETTLED, CLOSED)
        uint256 result; // Final result (PASSED, REJECTED, TIED)
    }
    // Proposal ID => Proposal
    mapping(uint256 => Proposal) public proposals;

    // Protocol token => Whether proposed
    // A protocol can only have one pool
    mapping(address => bool) public proposed;

    struct UserVote {
        uint256 choice; // 1: vote for, 2: vote against
        uint256 amount; // veHAL amount for voting
        bool claimed; // Voting reward already claimed
    }
    // User address => report id => user's voting info
    mapping(address => mapping(uint256 => UserVote)) public votes;

    // ---------------------------------------------------------------------------------------- //
    // ************************************* Constructor ************************************** //
    // ---------------------------------------------------------------------------------------- //

    constructor (
        address _deg,
        address _veDeg
    ) public {
        deg = IHalbornToken(_deg);
        veDeg = IVeHAL(_veDeg);

        deg.setOnboardProposal(address(this));
        veDeg.setOnboardProposal(address(this));

        owner = msg.sender;

        // Initial quorum 30%
        quorumRatio = 30;
    }

    // ---------------------------------------------------------------------------------------- //
    // ************************************ View Functions ************************************ //
    // ---------------------------------------------------------------------------------------- //

    function getProposal(uint256 _proposalId)
        external
        view
        returns (Proposal memory)
    {
        return proposals[_proposalId];
    }

    function getUserProposalVote(address _user, uint256 _proposalId)
        external
        view
        returns (UserVote memory)
    {
        return votes[_user][_proposalId];
    }

    function getAllProposals()
        external
        view
        returns (Proposal[] memory allProposals)
    {
        uint256 totalProposal = proposalCounter;

        allProposals = new Proposal[](totalProposal);

        for (uint256 i; i < totalProposal; ) {
            allProposals[i] = proposals[i + 1];

            unchecked {
                ++i;
            }
        }
    }

    // ---------------------------------------------------------------------------------------- //
    // ************************************ Set Functions ************************************* //
    // ---------------------------------------------------------------------------------------- //

    function setQuorumRatio(uint256 _quorumRatio) external onlyOwner {
        quorumRatio = _quorumRatio;
    }

    // ---------------------------------------------------------------------------------------- //
    // ************************************ Main Functions ************************************ //
    // ---------------------------------------------------------------------------------------- //


    /**
     * @notice Start a new proposal
     *
     * @param _name             New project name
     * @param _token            Native token address
     * @param _maxCapacity      Max capacity ratio for the project pool
     * @param _basePremiumRatio Base annual ratio of the premium
     */
    function propose(
        string calldata _name,
        address _token,
        uint256 _maxCapacity,
        uint256 _basePremiumRatio // 10000 == 100% premium annual cost
    ) external {
        _propose(_name, _token, _maxCapacity, _basePremiumRatio, msg.sender);
    }

    /**
     * @notice Vote for a proposal
     *
     *         Voting power is decided by the (unlocked) balance of veHAL
     *         Once voted, those veHAL will be locked
     *
     * @param _id     Proposal id
     * @param _isFor  Voting choice
     * @param _amount Amount of veHAL to vote
     */
    function vote(
        uint256 _id,
        uint256 _isFor,
        uint256 _amount
    ) external {
        _vote(_id, _isFor, _amount, msg.sender);
    }

    /**
     * @notice Settle the proposal result
     *
     * @param _id Proposal id
     */
    function settle(uint256 _id) external {
        Proposal storage proposal = proposals[_id];

        if (proposal.status != VOTING_STATUS)
            revert OnboardProposal__WrongStatus();

        if (!_passedVotingPeriod(proposal.proposeTimestamp))
            revert("No voting period passed");

        // If reached quorum, settle the result
        if (checkQuorum(proposal.numFor + proposal.numAgainst)) {
            uint256 res = _getVotingResult(
                proposal.numFor,
                proposal.numAgainst
            );

            // If this proposal not passed, allow new proposals for the same project
            // If it passed, not allow the same proposals
            if (res != PASS_RESULT) {
                // Allow for new proposals to be proposed for this protocol
                proposed[proposal.protocolToken] = false;
            }

            proposal.result = res;
            proposal.status = SETTLED_STATUS;

            emit ProposalSettled(_id, res);
        }
        // Else, set the result as "FAILED"
        else {
            proposal.result = FAILED_RESULT;
            proposal.status = SETTLED_STATUS;

            // Allow for new proposals to be proposed for this protocol
            proposed[proposal.protocolToken] = false;

            emit ProposalFailed(_id);
        }
    }

    /**
     * @notice Claim back veHAL after voting result settled
     *
     * @param _id Proposal id
     */
    function claim(uint256 _id) external {
        _claim(_id, msg.sender);
    }

    // ---------------------------------------------------------------------------------------- //
    // *********************************** Internal Functions ********************************* //
    // ---------------------------------------------------------------------------------------- //

    /**
     * @notice Start a new proposal
     *
     * @param _name             New project name
     * @param _token            Native token address
     * @param _maxCapacity      Max capacity ratio for the project pool
     * @param _basePremiumRatio Base annual ratio of the premium
     */
    function _propose(
        string calldata _name,
        address _token,
        uint256 _maxCapacity,
        uint256 _basePremiumRatio, // 10000 == 100% premium annual cost
        address _user
    ) internal {

        if (_maxCapacity == 0 || _maxCapacity > MAX_CAPACITY_RATIO)
            revert OnboardProposal__WrongCapacity();

        if (_basePremiumRatio >= 10000 || _basePremiumRatio == 0)
            revert OnboardProposal__WrongPremium();

        if (proposed[_token]) revert("Already proposed");

        // Burn Halborn tokens to start a proposal
        deg.burnHalborn(_user, PROPOSE_THRESHOLD);

        proposed[_token] = true;

        uint256 currentCounter = ++proposalCounter;
        // Record the proposal info
        Proposal storage proposal = proposals[currentCounter];
        proposal.name = _name;
        proposal.protocolToken = _token;
        proposal.proposer = _user;
        proposal.proposeTimestamp = block.timestamp;
        proposal.status = VOTING_STATUS;

        emit NewProposal(_name, _token, _user, _basePremiumRatio);
    }

    /**
     * @notice Vote for a proposal
     *
     * @param _id     Proposal id
     * @param _isFor  Voting choice
     * @param _amount Amount of veHAL to vote
     */
    function _vote(
        uint256 _id,
        uint256 _isFor,
        uint256 _amount,
        address _user
    ) internal {
        Proposal storage proposal = proposals[_id];

        // Should be manually switched on the voting process
        if (proposal.status != VOTING_STATUS)
            revert OnboardProposal__WrongStatus();
        if (_isFor != 1 && _isFor != 2) revert OnboardProposal__WrongChoice();
        if (_passedVotingPeriod(proposal.proposeTimestamp))
            revert("No voting period passed");
        if (_amount == 0) revert OnboardProposal__ZeroAmount();

        _enoughVeHAL(_user, _amount);

        // Lock vedeg until this report is settled
        veDeg.lockVeHAL(_user, _amount);

        // Record the user's choice
        UserVote storage userVote = votes[_user][_id];
        if (userVote.amount > 0) {
            if (userVote.choice != _isFor)
                revert OnboardProposal__ChooseBothSides();
        } else {
            userVote.choice = _isFor;
        }
        userVote.amount += _amount;

        // Record the vote for this report
        if (_isFor == 1) {
            proposal.numFor += _amount;
        } else {
            proposal.numAgainst += _amount;
        }

        emit ProposalVoted(_id, _user, _isFor, _amount);
    }

    /**
     * @notice Claim back veHAL after voting result settled
     *
     * @param _id Proposal id
     */
    function _claim(uint256 _id, address _user) internal {
        Proposal storage proposal = proposals[_id];

        if (proposal.status != SETTLED_STATUS)
            revert OnboardProposal__WrongStatus();

        UserVote storage userVote = votes[_user][_id];

        // Unlock the veHAL used for voting
        // No reward / punishment
        veDeg.unlockVeHAL(_user, userVote.amount);

        userVote.claimed = true;

        emit Claimed(_id, _user, userVote.amount);
    }

    /**
     * @notice Get the final voting result
     *
     * @param _numFor     Votes for
     * @param _numAgainst Votes against
     *
     * @return result Pass, reject or tied
     */
    function _getVotingResult(uint256 _numFor, uint256 _numAgainst)
        internal
        pure
        returns (uint256 result)
    {
        if (_numFor > _numAgainst) result = PASS_RESULT;
        else if (_numFor < _numAgainst) result = REJECT_RESULT;
        else result = TIED_RESULT;
    }

    /**
     * @notice Check whether has passed the voting time period
     *
     * @param _voteTimestamp Start timestamp of the voting
     *
     * @return hasPassed True for passing
     */
    function _passedVotingPeriod(uint256 _voteTimestamp)
        internal
        view
        returns (bool)
    {
        uint256 endTime = _voteTimestamp + PROPOSAL_VOTING_PERIOD;
        return block.timestamp > endTime;
    }

    /**
     * @notice Check quorum requirement
     *         30% of totalSupply is the minimum requirement for participation
     *
     * @param _totalVotes Total vote numbers
     */
    function checkQuorum(uint256 _totalVotes) public view returns (bool) {
        return _totalVotes >= (veDeg.totalSupply() * quorumRatio) / 100;
    }

    /**
     * @notice Check veHAL to be enough
     *         Only unlocked veHAL will be counted
     *
     * @param _user   User address
     * @param _amount Amount to fulfill
     */
    function _enoughVeHAL(address _user, uint256 _amount) internal view {
        uint256 unlockedBalance = veDeg.balanceOf(_user) - veDeg.locked(_user);
        if (unlockedBalance < _amount) revert OnboardProposal__NotEnoughVeHAL();
    }
}
