pragma solidity ^0.8.17;

contract BabyWallet {
    mapping(address => uint256) public balances;
    mapping(address => mapping(address => uint256)) public allowances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint256 amt) public {
        require(balances[msg.sender] >= amt, "You can't withdraw that much");
        balances[msg.sender] -= amt;
        (bool success, ) = msg.sender.call{value: amt}("");
        require(success, "Failed to withdraw that amount");
    }

    function approve(address recipient, uint256 amt) public {
        allowances[msg.sender][recipient] += amt;
    }

    function transfer(address recipient, uint256 amt) public {
        require(balances[msg.sender] >= amt, "You can't transfer that much");
        balances[msg.sender] -= amt;
        balances[recipient] += amt;
    }

    function transferFrom(address from, address to, uint256 amt) public {
        uint256 allowedAmt = allowances[from][msg.sender];
        uint256 fromBalance = balances[from];
        uint256 toBalance = balances[to];

        require(fromBalance >= amt, "You can't transfer that much");
        require(allowedAmt >= amt, "You don't have approval for that amount");

        balances[from] = fromBalance - amt;
        balances[to] = toBalance + amt;
        allowances[from][msg.sender] = allowedAmt - amt;
    }

    fallback() external payable {}
    receive() external payable {}
}