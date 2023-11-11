// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/utils/Strings.sol";

contract Bank {
    mapping (address => uint) public balances;
    mapping (address => uint) public nonces;

    event Deposit(address _from, uint256 _amount);
    event Withdrawal(address _to, uint256 _amount);
    event Transfer(address _from, address _to, uint256 _amount);

    constructor() {}

    function deposit() public payable {
        require(msg.value > 0);
        balances[msg.sender] += msg.value;
        emit Deposit(msg.sender, msg.value);
    }

    function withdraw(uint _amount) public {
        require(balances[msg.sender] >= _amount);
        balances[msg.sender] -= _amount;
        payable(msg.sender).transfer(_amount);
        emit Withdrawal(msg.sender, _amount);
    }

    function transfer(address _to, uint _amount) public {
        require(balances[msg.sender] >= _amount);
        require(_to != address(0));
        balances[msg.sender] -= _amount;
        balances[_to] += _amount;
        emit Transfer(msg.sender, _to, _amount);
    }

    function transferFrom(address _from, address _to, uint _amount, uint8 v, bytes32 r, bytes32 s) public {
        bytes32 message = keccak256(abi.encodePacked(Strings.toHexString(uint160(_from), 20), Strings.toString(_amount), Strings.toString(nonces[_from])));
        require(ecrecover(message, v, r, s) == _from);
        require(balances[_from] >= _amount);
        balances[_from] -= _amount;
        balances[_to] += _amount;
        nonces[_from] += 1;
        emit Transfer(_from, _to, _amount);
    }

    function burn(uint _amount) public {
        require(balances[msg.sender] >= _amount);
        balances[msg.sender] -= _amount;
        balances[address(0)] += _amount;
        emit Transfer(msg.sender, address(0), _amount);
    }
}
