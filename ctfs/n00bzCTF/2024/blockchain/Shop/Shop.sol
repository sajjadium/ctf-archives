pragma solidity ^0.6.0;
contract Shop {
    uint[4] cost = [5 ether,11 ether,23 ether,1337 ether];
   uint[4] bought = [0,0,0,0];
    function reset() public payable {
        bought[0] = 0;
        bought[1] = 0;
        bought[2] = 0;
        bought[3] = 0;
    }
    constructor() public {
        reset();
    }

    function buy(uint item, uint quantity) public payable {
        require(0 <= item && item<= 3, "Item does not exist!");
        require(0 < quantity && quantity <= 10, "Cannot buy more than 10 at once!");
        require(msg.value == (cost[item] * quantity), "Payment error!");
        bought[item] = quantity;
    }

    function refund(uint item, uint quantity) public payable {
        require(0 <= item && item <= 3, "Item does not exist!");
        require(0 < quantity && quantity <= 10, "Cannot refund more than 10 at once!");
        require(bought[item] > 0, "You do not have that item!");
        require(bought[item] >= quantity, "Quantity is greater than amount!");
        msg.sender.call.value((cost[item] * quantity))("");
        bought[item] -= quantity;
    }

    function isChallSolved() public view returns (bool solved) {
        if (bought[3] > 0) {
            return true;
        }
        else {
            return false;
        }
    }

}