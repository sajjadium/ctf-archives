// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

contract GlacierVault
{
    mapping(uint256 => address) slot_owners;
    mapping(uint256 => string) private slots;
    uint256 quickstore1;
    uint256 quickstore2;
    uint256 quickstore3;
    uint256 quickstore4;
    uint256 quickstore5;

    // You can use this vault to store your strings forever 
    function store(string memory item, uint256 slot_index) payable public
    {
        require(msg.value == 1337);
        require(slot_owners[slot_index] == address(0) || slot_owners[slot_index] == msg.sender, "this store is already used by someone else");

        slots[slot_index] = item;
        slot_owners[slot_index] = msg.sender;
    }

    //These are just for quickly storing numbers (like if you want to write down a phone number and don't forget it)
    function quickStore(uint8 index, uint256 value) public payable
    {
        require(msg.value == 1337);
        if(index == 0)
        {
            quickstore1 = value;
        }
        else if (index == 1)
        {
            quickstore2 = value;
        }
        else if (index == 2)
        {
            quickstore3 = value;
        }
        else if (index == 3)
        {
            quickstore4 = value;
        }
        else if (index == 4)
        {
            quickstore5 = value;
        }
    }
}