// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.19;

/**
 * ______                    _   _           _           _                     _
 * |  _  \                  | | | |         | |         | |                   | |
 * | | | |_____      ___ __ | | | |_ __   __| | ___ _ __| |     __ _ _ __   __| |
 * | | | / _ \ \ /\ / / '_ \| | | | '_ \ / _` |/ _ \ '__| |    / _` | '_ \ / _` |
 * | |/ / (_) \ V  V /| | | | |_| | | | | (_| |  __/ |  | |___| (_| | | | | (_| |
 * |___/ \___/ \_/\_/ |_| |_|\___/|_| |_|\__,_|\___|_|  \_____/\__,_|_| |_|\__,_|
 */

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";

contract AnotherPlease is ERC721Enumerable {
    uint256 public constant TICKETS_TO_GIVE_AWAY = 10;
    uint256 public constant PURCHASABLE_TICKETS = 20;

    uint256 public constant TICKET_PRICE = 10000000000000 ether;

    mapping(address => bool) public freeTicketReceivers;
    uint256 public ticketsGivenAway;

    error FreeTicketAlreadyClaimed();
    error FreeTicketsExhausted();
    error NotEnoughFunds();
    error SoldOut();

    constructor() ERC721("DownUnderLand Tickets", "DUCTF_ENTRY") {}

    modifier ticketNotClaimed() {
        if (freeTicketReceivers[msg.sender]) revert FreeTicketAlreadyClaimed();
        _;
    }

    // The first 20 people to claim a ticket get it freeeeeeeeeeeeeeeee!
    function claimFreeTicket() external ticketNotClaimed {
        if (ticketsGivenAway >= TICKETS_TO_GIVE_AWAY) revert FreeTicketsExhausted();
        _gibTicket(msg.sender);
        ticketsGivenAway++;
        freeTicketReceivers[msg.sender] = true;
    }

    // Buy a ticket to the exclusive DownUnderLand Party!!!!!
    // Cheap price!
    function buyATicket() external payable {
        if (msg.value < TICKET_PRICE) revert NotEnoughFunds();
        _gibTicket(msg.sender);

        uint256 change = TICKET_PRICE - msg.value;
        if (change > 0) {
            (bool success,) = msg.sender.call{value: change}("");
            require(success, "Bruh do u not want ur money back?");
        }
    }

    function totalTicketsAvailable() public pure returns (uint256) {
        return TICKETS_TO_GIVE_AWAY + PURCHASABLE_TICKETS;
    }

    function _gibTicket(address to) internal {
        if (totalSupply() >= totalTicketsAvailable()) revert SoldOut();
        _safeMint(to, totalSupply());
    }
}
