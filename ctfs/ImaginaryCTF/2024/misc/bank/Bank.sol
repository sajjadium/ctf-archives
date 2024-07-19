pragma solidity ^0.7.0;

contract Bank {
    uint48 flag_cost = 50;
    uint48 amount_you_have = 0;
    uint48 loaned = 0;
    function deposit(uint48 amount) public payable {
        require(msg.sender==YOUR_WALLET_ADDRESS,"Please use the wallet provided to you"); // This is for security purposes
    require(amount==msg.value,"Please send exact amount");
        amount_you_have += amount;
    }
    function withdraw(uint48 amount) public payable {
        require(msg.sender==YOUR_WALLET_ADDRESS,"Please use the wallet provided to you"); // This is for security purposes
        require((amount) < amount_you_have, "You cannot withdraw what you do not have!");
        amount_you_have -= amount;
        msg.sender.call{value:amount}("");
    }

    function getMoney() public payable {
        // Used for deployment, can be safely ignored
    }
    function loan(uint48 amount) public payable {
        require(msg.sender==YOUR_WALLET_ADDRESS,"Please use the wallet provided to you"); // This is for security purposes
        loaned += amount;
        msg.sender.call{value:amount}("");
    }

    function isChallSolved() public view returns (bool solved) {
        if ((amount_you_have >= flag_cost) && (loaned == 0)) {
            return true;
        }
        else {
            return false;
        }
    }


}