//SPDX-License-Identifier: MIT

// lfgggggg no registration eth chall

pragma solidity ^0.6.0;

contract TTMCoin {
	// the price of a single token is equal to the number of tokens in Wei
	// ex: if there are 15 tokens, the price of one token is 15 Wei

	uint public supply = 10;
	uint public price = 10 wei;

	string public name = "To the Moon Coin";
    string public symbol = "TTMCOIN";
	mapping (address => uint) public balanceOf;

	uint priceToBeat = 11 wei;
	bool public challIsSolved = false;

	function setPrice() public {
		price = supply * 1 wei;
	}

	function buy(uint _amount) public payable {
		require(_amount <= supply, "If this prints, the purchase amount is greater than the supply!");
		
		uint _tokensBought = msg.value/price;
		balanceOf[msg.sender] += _tokensBought;
		supply -= _tokensBought;
	}

	function solve() public {
		require(price > priceToBeat, "You have... NOT gone to the moon");
		challIsSolved = true;
	}
}
