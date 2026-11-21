// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./CouncilOfApes.sol";

contract IcyExchange
{
    TotallyNotCopiedToken public icyToken;
    CouncilOfApes public council;
    mapping (address => IcyPool) pools;
    mapping (address => mapping(IERC20 => uint256)) public liquidity;
    uint256 poolCounter;

    modifier onlyApe
    {
        require(council.getMemberClass(msg.sender) >= CouncilOfApes.apeClass.APE);
        _;
    }

    constructor() payable
    {
        require (msg.value == 5 ether, "You must pay 5 Ether to create the exchange");
        icyToken = new TotallyNotCopiedToken(address(this), "IcyToken", "ICY");
        council = new CouncilOfApes(address(icyToken));
    }

    //---------------------------- Public Functions ----------------------------//

    function createPool(address token) onlyApe() payable external
    {
        require(msg.value == 1 ether, "You must pay 1 Ether to create a pool");

        //Check if pool already exists
        require(address(pools[token]) == address(0), "This pool already exists");

        //Create the pool and add it to the pools mapping
        pools[token] = new IcyPool(address(icyToken), token);
        
        //Every pool needs to be initialized with 100,000 of the chosen tokens and will get 100,000 of the icyToken
        IERC20(token).transferFrom(msg.sender, address(pools[token]), 100_000);
        icyToken.transfer(address(pools[token]), 100_000);
    }

    function swap(address fromToken, address toToken, uint256 amount) onlyApe() external
    {
        require(amount > 0, "You must swap at least 1 token");

        IcyPool pool;

        if(fromToken == address(icyToken))
        {
            pool = pools[toToken];
        }
        else if (toToken == address(icyToken))
        {
            pool = pools[fromToken]; 
        }

        pool.swap(msg.sender, fromToken, toToken, amount);
    }

    //---------------------------- Lending Functions ----------------------------//

    //We offer the worlds first collateralized flash loan (even safer than anything else)
    function collateralizedFlashloan(address collateralToken, uint256 amount, address target) onlyApe() external
    {
        require(amount > 0, "You must lend out at least 1 token");
        require(amount <= icyToken.balanceOf(address(this)), "We can't lend you this much");
        require(IERC20(collateralToken).totalSupply() <= 100_000_000, "Shitcoins are not accepted");
        require(address(pools[collateralToken]) != address(0), "This pool does not exist");

        uint256 neededCollateral = pools[collateralToken].getTokensPerIcyToken(amount);
        require(neededCollateral <= 100_000_000, "Shitcoins are still not accepted, don't try to cheat us");

        //Receive the collateral
        IERC20(collateralToken).transferFrom(msg.sender, address(this), neededCollateral);

        //Flashloan happens
        icyToken.transfer(msg.sender, amount);

        //You get to do stuff
        (bool success, ) = target.call(abi.encodeWithSignature("receiveFlashLoan(uint256)", amount));
        require(success);

        //By here we should get all our money back
        icyToken.transferFrom(msg.sender, address(this), amount);

        //Return the collateral
        IERC20(collateralToken).transfer(msg.sender, neededCollateral);
    }

    //---------------------------- View Functions ----------------------------//

    function getPoolCount() public view returns (uint256)
    {
        return poolCounter;
    }

    function getPool(address token) public view returns (IcyPool)
    {
        return pools[token];
    }
}