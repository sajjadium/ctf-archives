// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Address.sol";

contract PETH is Ownable {
    using Address for address;
    using Address for address payable;

    string public constant name = "Pigeon ETH";
    string public constant symbol = "PETH";
    uint8 public constant decimals = 18;

    event Approval(address indexed src, address indexed dst, uint256 amt);
    event Transfer(address indexed src, address indexed dst, uint256 amt);
    event Deposit(address indexed dst, uint256 amt);
    event Withdrawal(address indexed src, uint256 amt);

    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    receive() external payable {
        revert("PETH: Do not send ETH directly");
    }

    function deposit(address _userAddress) public payable onlyOwner {
        _mint(_userAddress, msg.value);
        emit Deposit(_userAddress, msg.value);
        // return msg.value;
    }

    function withdraw(address _userAddress, uint256 _wad) public onlyOwner {
        payable(_userAddress).sendValue(_wad);
        _burn(_userAddress, _wad);
        // require(success, "SEETH: withdraw failed");
        emit Withdrawal(_userAddress, _wad);
    }

    function withdrawAll(address _userAddress) public onlyOwner {
        payable(_userAddress).sendValue(balanceOf[_userAddress]);
        _burnAll(_userAddress);
        // require(success, "SEETH: withdraw failed");
        emit Withdrawal(_userAddress, balanceOf[_userAddress]);
    }

    function totalSupply() public view returns (uint256) {
        return address(this).balance;
    }

    function approve(address guy, uint256 wad) public returns (bool) {
        allowance[msg.sender][guy] = wad;
        emit Approval(msg.sender, guy, wad);
        return true;
    }

    function transfer(address dst, uint256 wad) public returns (bool) {
        return transferFrom(msg.sender, dst, wad);
    }

    function transferFrom(address src, address dst, uint256 wad) public returns (bool) {
        require(balanceOf[src] >= wad);

        if (src != msg.sender && allowance[src][msg.sender] != type(uint256).max) {
            require(allowance[src][msg.sender] >= wad);
            allowance[src][msg.sender] -= wad;
        }

        balanceOf[src] -= wad;
        balanceOf[dst] += wad;

        emit Transfer(src, dst, wad);

        return true;
    }

    function flashLoan(address _userAddress, uint256 _wad, bytes calldata data) public onlyOwner {
        require(_wad <= address(this).balance, "PETH: wad exceeds balance");
        require(Address.isContract(_userAddress), "PETH: Borrower must be a contract");

        uint256 userBalanceBefore = address(this).balance;

        // @dev Send Ether to borrower (Borrower must implement receive() function)
        Address.functionCallWithValue(_userAddress, data, _wad);

        uint256 userBalanceAfter = address(this).balance;

        require(userBalanceAfter >= userBalanceBefore, "PETH: You did not return my Ether!");

        // @dev if user gave me more Ether, refund it
        if (userBalanceAfter > userBalanceBefore) {
            uint256 refund = userBalanceAfter - userBalanceBefore;
            payable(_userAddress).sendValue(refund);
        }
    }

    // ========== INTERNAL FUNCTION ==========

    function _mint(address dst, uint256 wad) internal {
        balanceOf[dst] += wad;
    }

    function _burn(address src, uint256 wad) internal {
        require(balanceOf[src] >= wad);
        balanceOf[src] -= wad;
    }

    function _burnAll(address _userAddress) internal {
        _burn(_userAddress, balanceOf[_userAddress]);
    }
}
