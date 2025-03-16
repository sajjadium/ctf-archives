// SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.28;
contract BankOfBankruptcy {

	mapping(address => int256) balance;
	mapping(address => mapping(address => uint256)) allow;
	mapping(address => bool) lock;
	mapping(address => bool) registered;
	mapping(address => uint256) claims;
	uint256 MAX_AMOUNT = 1000;
	
	event BankruptcyClaim(address who, uint256 claimID);
	constructor () {
    }

	modifier notReentrant(){
		require(!lock[msg.sender],"Nope");
		_;
	}

	modifier withinLimit(uint256 amount){
		require(amount <= MAX_AMOUNT,"Amount must be within limit");
		_;
	}

	modifier requireRegistration(address addr) {
		require(registered[addr],"Address is not registered");
		_; 
	}

	function allowTransfer(address dest, uint256 amount) public withinLimit(amount) requireRegistration(dest) requireRegistration(msg.sender){
		allow[msg.sender][dest] += amount;
	}
	
	function transferFrom(address from, uint256 amount) public withinLimit(amount) requireRegistration(from) requireRegistration(msg.sender){
		require(balance[from] >= int256(amount), "Sender has not enough $$");
		require(allow[from][msg.sender] >= amount, "Not Enough allowance");
		balance[from] -= int256(amount);
		allow[from][msg.sender] -= amount;
		balance[msg.sender] += int256(amount);
	}

	function withdraw(uint256 amount) public notReentrant withinLimit(amount) requireRegistration(msg.sender){
		lock[msg.sender] = true;
		require(balance[msg.sender] >= int256(amount),"Not enough balance");
		(bool status, ) = msg.sender.call("withdrawCallback");
        require(status, "Reverting...");
		balance[msg.sender] -= int256(amount);
		lock[msg.sender] = false;
	}

	function register() public {
		require(!registered[msg.sender],"Already Registered");
		balance[msg.sender] = 1000;
		registered[msg.sender] = true;
	}

	function fileBankruptcy(uint256 caseNumber) public requireRegistration(msg.sender){
		require(balance[msg.sender] < 0, "You are not bankrupt... yet.");
		claims[msg.sender] = caseNumber;
		emit BankruptcyClaim(msg.sender,caseNumber);
	}

	function getCaseNumber(address addr) public view requireRegistration(addr) returns (uint256){
		return claims[addr];
	}
}