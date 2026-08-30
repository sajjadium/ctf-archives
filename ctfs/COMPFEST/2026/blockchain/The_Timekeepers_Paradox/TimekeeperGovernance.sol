// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./TimekeeperToken.sol";

contract TimekeeperGovernance {
    TimekeeperToken public token;
    address public oracleProxy;
    address public lendingPool;
    
    uint256 public constant TIMELOCK = 7 days;
    uint256 public constant QUORUM_BPS = 5100;
    uint256 public constant BPS_PRECISION = 10000;

    struct Proposal {
        uint256 id;
        address proposer;
        string description;
        bytes callData;
        address target;
        uint256 votesFor;
        uint256 votesAgainst;
        uint256 createdAt;
        uint256 executionTime;
        bool executed;
        bool cancelled;
    }

    uint256 public proposalCount;
    mapping(uint256 => Proposal) public proposals;
    mapping(uint256 => mapping(address => bool)) public hasVoted;

    event ProposalCreated(uint256 indexed id, address indexed proposer, string description);
    event Voted(uint256 indexed id, address indexed voter, bool support, uint256 weight);
    event ProposalExecuted(uint256 indexed id);
    event ProposalCancelled(uint256 indexed id);

    constructor(address _token, address _oracleProxy, address _lendingPool) {
        token = TimekeeperToken(_token);
        oracleProxy = _oracleProxy;
        lendingPool = _lendingPool;
    }

    function propose(
        string calldata description,
        address target,
        bytes calldata callData
    ) external returns (uint256) {
        require(token.balanceOf(msg.sender) > 0, "Must hold tokens to propose");

        proposalCount++;
        uint256 id = proposalCount;

        proposals[id] = Proposal({
            id: id,
            proposer: msg.sender,
            description: description,
            callData: callData,
            target: target,
            votesFor: 0,
            votesAgainst: 0,
            createdAt: block.timestamp,
            executionTime: 0,
            executed: false,
            cancelled: false
        });

        emit ProposalCreated(id, msg.sender, description);
        return id;
    }

    function vote(uint256 proposalId, bool support) external {
        Proposal storage prop = proposals[proposalId];
        require(prop.id != 0, "Proposal doesn't exist");
        require(!prop.executed, "Already executed");
        require(!prop.cancelled, "Proposal cancelled");
        require(!hasVoted[proposalId][msg.sender], "Already voted");
        
        uint256 weight = token.balanceOf(msg.sender);
        require(weight > 0, "No voting power");

        hasVoted[proposalId][msg.sender] = true;

        if (support) {
            prop.votesFor += weight;
        } else {
            prop.votesAgainst += weight;
        }

        uint256 quorum = (token.totalSupply() * QUORUM_BPS) / BPS_PRECISION;
        if (prop.votesFor >= quorum && prop.executionTime == 0) {
            prop.executionTime = block.timestamp + TIMELOCK;
        }

        emit Voted(proposalId, msg.sender, support, weight);
    }

    function execute(uint256 proposalId) external {
        Proposal storage prop = proposals[proposalId];
        require(prop.id != 0, "Proposal doesn't exist");
        require(!prop.executed, "Already executed");
        require(!prop.cancelled, "Proposal cancelled");
        require(prop.executionTime > 0, "Quorum not reached");
        require(block.timestamp >= prop.executionTime, "Timelock not expired");

        prop.executed = true;

        (bool success, ) = prop.target.call(prop.callData);
        require(success, "Execution failed");

        emit ProposalExecuted(proposalId);
    }

    function setOracleReporter(address newReporter) external {
        require(msg.sender == address(this), "Only governance");
        // Would call oracle.setReporter(newReporter) if executed
        (bool success, ) = oracleProxy.call(
            abi.encodeWithSignature("setReporter(address)", newReporter)
        );
        require(success, "Failed to set reporter");
    }

    function upgradeProxy(address newImplementation) external {
        require(msg.sender == address(this), "Only governance");
        (bool success, ) = oracleProxy.call(
            abi.encodeWithSignature("upgradeTo(address)", newImplementation)
        );
        require(success, "Failed to upgrade");
    }

    function emergencyPause() external {
        require(msg.sender == address(this), "Only governance");
        // Would pause the lending pool
    }
}
