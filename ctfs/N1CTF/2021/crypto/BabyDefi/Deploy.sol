pragma solidity ^0.6.12;
import "./ERC20.sol";
import "./SimpleSwap.sol";
import "./N1Farm.sol";
import "./FlashLoan.sol";
// import "./Context.sol";

interface IN1Farm{
    function getUserAmount(address) external returns(uint)  ;
} 

contract Deploy{

    address public farm;
    address public flagtoken;

    event TOKENA(address);
    event TOKENB(address);
    event POOL(address);
    event N1FARM(address);
    event FLASHLOAN(address);
    event SendFlag(address user);

    uint256 private constant target = 200000000000000000000000;
    constructor() public {
        // tokens
        N1Token n1Token = new N1Token();
        FlagToken flagToken = new FlagToken();
        emit TOKENA(address(n1Token));
        emit TOKENB(address(flagToken));
        flagtoken = address(flagToken);
        // init
        SimpleSwapPair simpleSwap = new SimpleSwapPair(address(n1Token),address(flagToken));
        emit POOL(address(simpleSwap));
        n1Token.mint(address(simpleSwap),90000000000000000000000);
        flagToken.mint(address(simpleSwap),90000000000000000000000);
        simpleSwap.mint(address(this));
        // init n1Farm
        N1Farm n1Farm = new N1Farm(address(n1Token),address(flagToken),address(simpleSwap));
        farm = address(n1Farm);
        emit N1FARM(address(n1Farm));
        n1Token.mint(address(n1Farm),6000000000000000000000);
        flagToken.transferOwnership(address(n1Farm));
        // mint to flashloan
        FlashLoan floan = new FlashLoan(address(n1Token));
        emit FLASHLOAN(address(floan));
        n1Token.mint(address(floan),4000000000000000000000);
    }
    
    function isSolved() public {
        require(IN1Farm(farm).getUserAmount(msg.sender) > 0,"Haven't deposited.");
        require(IERC20(flagtoken).balanceOf(msg.sender) > target,"FlagToken Not enough");
        emit SendFlag(address(this));
    }
}
