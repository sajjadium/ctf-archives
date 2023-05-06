// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./openzeppelin/contracts/access/Ownable.sol";

contract SakuraContract is Ownable {
    address payable private fee_account;
    
    uint private max_holders;
    uint256 private amount;
    string private description;

    uint256 private fixed_fee;
    uint256 amount_after_feecalc;

    struct Deposit {
        uint256 locked_eth;
        uint16 answer;
        uint16 judge;
    }

    address[] internal keyList;
    mapping(address => Deposit) private depositInfo;

    enum State { Created, Cancelled, WaitingWinnerSelect, WaitingAdminApproval, Closed }
    State private state;

    event Locked(address from, uint256 amount, uint answer);
    event UserJudged(address from, uint16 _answer);
    event AdminApprovalRequired();
    event AdminApproved(uint16 _answer);
    event Closed();
    event Cancelled();

    receive() external payable { revert(); }

    constructor(address _admin_account,
                address payable _fee_account, 
                string memory _description, 
                uint _max_holders, 
                uint256 _amount,
                uint256 _fixed_fee)
    {
        description = _description;
        amount = _amount;

        max_holders = _max_holders;

        state = State.Created;

        fee_account = _fee_account;
        fixed_fee = _fixed_fee;
        amount_after_feecalc = amount - _fixed_fee;

        transferOwnership(_admin_account);
    }

    modifier onlyPublicHolders() {
        if (owner() == msg.sender)
            _;

        require( keyList.length <= max_holders, "Already occupied" );
        _;
    }

    modifier onlyHolders() {
        if (owner() == msg.sender)
            _;

        require( depositInfo[msg.sender].locked_eth > 0, "Only holders can call this");
        _;
    }
 
    modifier inState(State _state) {
        require(
            state == _state,
            "Invalid state"
        );
        _;
    }

    function getLockedList() external view returns (address[] memory) {
        return keyList;
    }

    function getLocked() external view returns (uint256) {
        return depositInfo[msg.sender].locked_eth;
    }
    
    function close(uint16 _answer) private {
        require(state != State.Closed, "Sakura contract already closed");

        state = State.Closed;

        for (uint i = 0; i < keyList.length; i++) {
            address payable holder_address = payable(address(uint160(keyList[i])));
            Deposit storage holder = depositInfo[keyList[i]];
            uint256 calc = 0;

            if (holder.answer == _answer) {
                calc = holder.locked_eth + amount_after_feecalc;
            } else {
                require(holder.locked_eth >= amount, "Invalid loser amount?");
                calc = holder.locked_eth - amount;
            }

            holder.locked_eth = 0;
            holder_address.call{value: calc}("");
        }

        selfdestruct(payable(fee_account));
        emit Closed();
    }

    function adminJudge(uint16 _answer) external onlyOwner {
        close(_answer);
        emit AdminApproved(_answer);
    }

    function userJudge(uint16 _answer) external onlyHolders inState(State.WaitingWinnerSelect) {
        require( depositInfo[msg.sender].judge == 0, "You already selected an answer" );

        depositInfo[msg.sender].judge = _answer;

        bool is_unanimous = true;
        uint256 judge_complete = 0;

        for (uint i = 0; i < keyList.length; i++) {
            if (depositInfo[keyList[i]].judge != 0) {
                judge_complete ++;
            }

            if (depositInfo[keyList[i]].judge != _answer) {
                is_unanimous = false;
            }
        }

        if (judge_complete != max_holders) {
            emit UserJudged(msg.sender, _answer);
            return; // still voting
        }

        if (is_unanimous == true) {
            close(_answer);
            return;
        }

        state = State.WaitingAdminApproval;
        emit AdminApprovalRequired();
    }

    function revoke() external onlyHolders payable inState(State.Cancelled) {
        require(depositInfo[msg.sender].locked_eth >= amount, "Invalid amount?");

        uint256 _amount = depositInfo[msg.sender].locked_eth;

        depositInfo[msg.sender].locked_eth = 0;

        payable(msg.sender).call{value: _amount}("");
    }

    function cancelByAdmin() external onlyOwner {
        require(state != State.Closed, "Invalid cancel");
        state = State.Cancelled;
        emit Cancelled();
    }

    function cancelByUser() external onlyHolders {
        require(state == State.Created || state == State.WaitingWinnerSelect, "You cannot cancel");
        state = State.Cancelled;
        emit Cancelled();
    }

    function lock(uint16 _answer) external onlyPublicHolders inState(State.Created) payable {
        require(depositInfo[msg.sender].locked_eth == 0, "Locked deposit must be zero");
        require(depositInfo[msg.sender].answer == 0, "You can only answer once");
        require(_answer != 0, "Answer must not be zero");
        require(_answer == 1 || _answer == 2, "Answer must be 1 or 2");

        require(msg.value >= amount && msg.value > 0, "Must send equal or higher than amount");
        require(msg.value < (amount * 2), "Betting amount is too much");

        keyList.push(msg.sender);

        if (keyList.length == max_holders) {
            state = State.WaitingWinnerSelect;
        }

        depositInfo[msg.sender].locked_eth = msg.value;
        depositInfo[msg.sender].answer = _answer;
        emit Locked(msg.sender, msg.value, _answer);
    }
}




