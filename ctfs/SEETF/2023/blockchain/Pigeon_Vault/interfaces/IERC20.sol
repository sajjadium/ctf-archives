// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;

interface IERC20 {
    struct Checkpoint {
        uint32 fromBlock;
        uint256 votes;
    }

    function name() external pure returns (string memory);
    function symbol() external pure returns (string memory);
    function decimals() external pure returns (uint8);
    function totalSupply() external view returns (uint256);
    function balanceOf(address _account) external view returns (uint256);
    function allowance(address _account, address _spender) external view returns (uint256);
    function mint(address _to, uint256 _amount) external;
    function approve(address _spender, uint256 _amount) external returns (bool);
    function transfer(address _to, uint256 _amount) external returns (bool);
    function transferFrom(address _from, address _to, uint256 _amount) external returns (bool);
    function delegate(address _delegatee) external;
    function getCurrentVotes(address _account) external view returns (uint256);
    function getNumberOfCheckpoints(address _account) external view returns (uint32);
    function getCheckpoint(address _account, uint32 _pos) external view returns (Checkpoint memory);
    function getPriorVotes(address _account, uint256 _blockNumber) external view returns (uint256);
}
