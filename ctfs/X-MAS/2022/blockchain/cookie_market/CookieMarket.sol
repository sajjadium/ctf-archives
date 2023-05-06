// SPDX-License-Identifier: MIT
pragma solidity 0.8.17;

import "./IERC721.sol";
import "./IERC721Receiver.sol";

contract CookieMarket is IERC721Receiver {

    // mapping that handles ownership of the cookies within the CookieMarket.
    mapping(uint256 => address) public canRedeemcookie;
    
    // struct that handles the orders in the market
    struct sell_Order {
        uint256 cookie_idx_offered;    // the ERC721 idx of the "cookie" token.
        uint256 amount_eth_wanted;  // the amount of ETH the seller wants to receive for the cookie.
        address cookie_provider;       // the address of the seller.
    }

    // storing all the sell orders in the market.
    sell_Order[] public sellOrders;

    // cookie
    IERC721 public cookie;
    
    /**
        @dev cookieMarket constructor.

        @param _cookie ERC721 contract instance.
    */
    constructor(address _cookie) {
        cookie = IERC721(_cookie);
    }

    /**
        @dev Allows a buyer to buy an cookie from the cookieMarket via exhausting its subsequent sell order.

        @param _idx The ERC721 idx of the cookie.
        @param _owner The `current` owner of the cookie.
    */
    function executeOrder(uint256 _idx, address _owner) external payable {

        require(
            msg.sender != _owner, 
            "err: no self-exchanges allowed"
        );

        // find the sellOrder whose cookie_idx_offered == _idx
        for (uint256 i = 0; i < sellOrders.length; i++) {
            if (sellOrders[i].cookie_idx_offered == _idx) {

                // check if the _owner is the seller
                require(sellOrders[i].cookie_provider == _owner, "err: _owner != seller");

                // the cookie is for sale.
                
                // check if the msg.sender has provided enough ETH to pay for the cookie
                if (msg.value >= sellOrders[i].amount_eth_wanted) {

                    // the _owner has enough ETH to pay for the cookie
                    // paying the seller(current owner) of the cookie
                    (bool sent, bytes memory data) = _owner.call{value: msg.value}("");
                    require(sent, "err: transfer failed");

                    // transfer the ownership of the cookie from the seller to the buyer
                    canRedeemcookie[_idx] = msg.sender;

                    // remove the sellOrder from the sellOrders array
                    sellOrders[i] = sellOrders[sellOrders.length - 1];
                    sellOrders.pop();

                    break;
                }
            }
        }
    }

    /**
        @dev Function to retrieve an cookie from the market.
        
        @param _idx The index of the cookie in the market.
    */
    function redeemcookies(uint256 _idx) external {

        // check if sender can redeem the cookie
        require(
            canRedeemcookie[_idx] == msg.sender,
            "err: msg.sender != owner(cookie)"
        );

        // approve the cookie transfer.
        cookie.approve(
            msg.sender, 
            _idx
        );

        // transfer the ownership of the cookie.
        cookie.transferFrom(
            address(this), 
            msg.sender, 
            _idx
        );

        // remove the cookie _idx from the canRedeemcookie mapping
        delete canRedeemcookie[_idx];
    }

    /**
        @dev Function to effectively add a sellOrder for your cookie on the cookieMarket.
        
        @param _cookieIDX The index of the ERC721 cookie.
        @param _ethWanted The amount of ETH the seller wants to receive for the cookie.
    */
    function addSellOrder(uint256 _cookieIDX, uint256 _ethWanted) external {

        // check whether the msg.sender can sell the _cookieIDX
        require(
            canRedeemcookie[_cookieIDX] == msg.sender,
            "err: msg.sender != owner(cookie[_cookieIDX])"
        );

        // create the new sellOrder
        sell_Order memory newOrder;
        newOrder.cookie_idx_offered = _cookieIDX;
        newOrder.amount_eth_wanted = _ethWanted;
        newOrder.cookie_provider = msg.sender;

        sellOrders.push(newOrder);
    }

    /**
        @dev Function to effectively remove a sellOrder from the cookieMarket.
        
        @param _cookieIDX The index of the ERC721 cookie.
    */
    function removeSellOrder(uint256 _cookieIDX) external {

        // iterate through all sellOrders
        for(uint256 i = 0; i < sellOrders.length; i++) {

            // check if the sellOrder is for the _cookieIDX
            if (sellOrders[i].cookie_idx_offered == _cookieIDX) {
                
                // check if the msg.sender is the owner of the cookie
                require(
                    sellOrders[i].cookie_provider == msg.sender,
                    "err: msg.sender != cookie_provider"
                );

                // delete the sellOrder
                sellOrders[i] = sellOrders[sellOrders.length - 1];
                sellOrders.pop();
                break;
            }
        }
    }

    /**
        @dev Inherited from IERC721Receiver.
    */
    function onERC721Received(
        address,
        address _from,
        uint256 _tokenId,
        bytes calldata
    ) external override returns (bytes4) {

        // we have received an cookie from its owner; mark that in the redeem mapping
        canRedeemcookie[_tokenId] = _from;
        
        return this.onERC721Received.selector; 
    }
}