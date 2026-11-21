pragma solidity ^0.8.20;

import "./IcyPool.sol";

contract CouncilOfApes
{
    mapping (address => uint256) public bananaBalance;
    mapping (address => uint256) public votes;
    mapping (address => apeClass) public members;

    bool public dissolved;
    IERC20 public icyToken;
    uint256 lastVote;

    enum apeClass{
        NOBODY,
        APE,
        CHIMP,
        ORANGUTAN,
        GORILLA
    }

    modifier notDissolved
    {
        require(dissolved == false, "The council has been dissolved");
        _;
    }

    modifier onlyAlpha
    {
        require(members[msg.sender] == apeClass.GORILLA, "This function can only be called by an alpha ape");
        _;
    }

    constructor(address _icyToken)
    {
        dissolved = false;
        icyToken = IERC20(_icyToken);
        lastVote = 0;
    }

    //--------------------------- APE FUNCTIONS ---------------------------//

    //To become an ape you have to say the holy words.
    function becomeAnApe(bytes32 theHolyWords) external notDissolved
    {
        require(theHolyWords == keccak256("I hereby swear to ape into every shitcoin I see, to never sell, to never surrender, to never give up, to never stop buying, to never stop hodling, to never stop aping, to never stop believing, to never stop dreaming, to never stop hoping, to never stop loving, to never stop living, to never stop breathing"));

        //You are officially an ape now
        members[msg.sender] = apeClass.APE;

        //You get a free banana
        bananaBalance[msg.sender] = 1;
    }

    //You can also buy bananas from the apes
    function buyBanana(uint256 amount) external notDissolved() 
    {
        require(members[msg.sender] == apeClass.APE);

        icyToken.transferFrom(msg.sender, address(this), amount);
        bananaBalance[msg.sender] += amount;
    }

    //You can also get your bananas back
    function sellBanana(uint256 amount) external notDissolved()
    {
        require(bananaBalance[msg.sender] >= amount, "You don't have that many bananas");

        icyToken.transfer(msg.sender, amount);
        bananaBalance[msg.sender] -= amount;
    }

    //Every cycle the apes vote for new alphas with their bananas
    function vote(address target, uint256 amount) external
    {
        require(bananaBalance[msg.sender] >= amount, "You don't have that many bananas");
        bananaBalance[msg.sender] -= amount;
        votes[target] += amount;
    }

    //If you have enough votes, you can claim a new rank
    function claimNewRank() external
    {
        if (votes[msg.sender] >= 1_000_000_000)
        {
            members[msg.sender] = apeClass.GORILLA;
            lastVote = block.timestamp;
        }
        else if (votes[msg.sender] >= 1_000_000)
        {
            members[msg.sender] = apeClass.ORANGUTAN;
            lastVote = block.timestamp;
        } 
        else if (votes[msg.sender] >= 1_000)
        {
            members[msg.sender] = apeClass.CHIMP;
            lastVote = block.timestamp;
        } 
    }

    //--------------------------- ALPHA FUNCTIONS ---------------------------//

    //The alpha can issue himself bananas
    function issueBanana(uint256 amount, address target) external notDissolved() onlyAlpha()
    {
        require(amount > 0, "You must issue at least 1 banana");

        bananaBalance[target] += amount;
    }

    //If you are one of the alpha apes, you can dissolve the council
    function dissolveCouncilOfTheApes(bytes32 theEvilWords) external notDissolved() onlyAlpha()
    {
        require(theEvilWords == keccak256("Kevin come out of the basement, dinner is ready."));

        dissolved = true;
    }

    //--------------------------- VIEW FUNCTIONS ---------------------------//

    function getBananaBalance(address target) external view returns (uint256)
    {
        return bananaBalance[target];
    }

    function getVotes(address target) external view returns (uint256)
    {
        return votes[target];
    }

    function getMemberClass(address target) external view returns (apeClass)
    {
        return members[target];
    }

    function isDissolved() external view returns (bool)
    {
        return dissolved;
    }
}