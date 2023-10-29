// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "./Token.sol";

contract TokenFactory {
    address public router;

    mapping(address => bool) public tokens;
    address[] public allTokens;

    modifier onlyRouter() {
        require(msg.sender == router);
        _;
    }

    constructor() {
        router = msg.sender;
    }

    function createToken(string memory _tokenName, string memory _tokenSymbol)
        external
        onlyRouter
        returns (address _token)
    {
        _token = address(new Token(_tokenName, _tokenSymbol));
        tokens[_token] = true;
        allTokens.push(_token);
    }

    function tokenMint(address token, address to, uint256 amount) external onlyRouter {
        Token(token).mint(to, amount);
    }
}
