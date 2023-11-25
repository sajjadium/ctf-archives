// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

import "./Ticket.sol";

contract ChairLift
{
    uint256 public tripsTaken;
    Ticket public ticket;
    address owner;

    constructor ()
    {
        ticket = new Ticket("Chairlift Ticket");
        owner = msg.sender;
    }

    //To get a ride you have to buy a ticket first
    function buyTicket() external payable
    {
        if (msg.sender != owner)
        {
            require (msg.value == 100_000 ether, "Ticket costs 100,000 ether, inflation has been hitting us hard too");
        }
        
        ticket.mint(msg.sender);
    } 

    //USing your ticket you can take a ride on the chairlift
    function takeRide(uint256 ticketId) external
    {
        require (ticket.ownerOf(ticketId) == msg.sender, "You don't own this ticket");

        tripsTaken += 1;
        ticket.burn(ticketId);
    }
}