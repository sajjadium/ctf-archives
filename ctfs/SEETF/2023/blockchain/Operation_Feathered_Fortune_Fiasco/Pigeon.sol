// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.17;

contract Pigeon {
    address private owner;
    uint256 private ownerBalance;
    uint256 private juniorPromotion;
    uint256 private associatePromotion;

    mapping(bytes32 => address) private seniorPigeon;
    mapping(bytes32 => address) private associatePigeon;
    mapping(bytes32 => address) private juniorPigeon;
    mapping(address => bool) private isPigeon;
    mapping(string => mapping(string => bool)) private codeToName;
    mapping(bytes32 => uint256) private taskPoints;

    mapping(address => mapping(address => uint256)) private dataCollection;
    mapping(address => bool) private hasBeenCollected;
    mapping(bytes32 => uint256) private treasury;

    modifier onlyOwner() {
        if (owner != msg.sender) revert();
        _;
    }

    modifier oneOfUs() {
        if (!isPigeon[msg.sender]) revert();
        _;
    }

    constructor() {
        owner = msg.sender;
        juniorPromotion = 8e18;
        associatePromotion = 12e18;
    }

    function becomeAPigeon(string memory code, string memory name) public returns (bytes32 codeName) {
        codeName = keccak256(abi.encodePacked(code, name));

        if (codeToName[code][name]) revert();
        if (isPigeon[msg.sender]) revert();

        juniorPigeon[codeName] = msg.sender;
        isPigeon[msg.sender] = true;
        codeToName[code][name] = true;

        return codeName;
    }

    function task(bytes32 codeName, address person, uint256 data) public oneOfUs {
        if (person == address(0)) revert();
        if (isPigeon[person]) revert();
        if (address(person).balance != data) revert();

        uint256 points = data;

        hasBeenCollected[person] = true;
        dataCollection[msg.sender][person] = points;
        taskPoints[codeName] += points;
    }

    function flyAway(bytes32 codeName, uint256 rank) public oneOfUs {
        uint256 bag = treasury[codeName];
        treasury[codeName] = 0;

        if (rank == 0) {
            if (taskPoints[codeName] > juniorPromotion) revert();

            (bool success,) = juniorPigeon[codeName].call{value: bag}("");
            require(success, "Transfer failed.");
        }
        if (rank == 1) {
            if (taskPoints[codeName] > associatePromotion) revert();

            (bool success,) = associatePigeon[codeName].call{value: bag}("");
            require(success, "Transfer failed.");
        }
        if (rank == 2) {
            (bool success,) = seniorPigeon[codeName].call{value: bag}("");
            require(success, "Transfer failed.");
        }
    }

    function promotion(bytes32 codeName, uint256 desiredRank, string memory newCode, string memory newName)
        public
        oneOfUs
    {
        if (desiredRank == 1) {
            if (msg.sender != juniorPigeon[codeName]) revert();
            if (taskPoints[codeName] < juniorPromotion) revert();
            ownerBalance += treasury[codeName];

            bytes32 newCodeName = keccak256(abi.encodePacked(newCode, newName));

            if (codeToName[newCode][newName]) revert();
            associatePigeon[newCodeName] = msg.sender;
            codeToName[newCode][newName] = true;
            taskPoints[codeName] = 0;
            delete juniorPigeon[codeName];

            (bool success,) = owner.call{value: treasury[codeName]}("");
            require(success, "Transfer failed.");
        }

        if (desiredRank == 2) {
            if (msg.sender != associatePigeon[codeName]) revert();
            if (taskPoints[codeName] < associatePromotion) revert();
            ownerBalance += treasury[codeName];

            bytes32 newCodeName = keccak256(abi.encodePacked(newCode, newName));

            if (codeToName[newCode][newName]) revert();
            seniorPigeon[newCodeName] = msg.sender;
            codeToName[newCode][newName] = true;
            taskPoints[codeName] = 0;
            delete seniorPigeon[codeName];

            (bool success,) = owner.call{value: treasury[codeName]}("");
            require(success, "Transfer failed.");
        }
    }

    function assignPigeon(string memory code, string memory name, address pigeon, uint256 rank)
        external
        payable
        onlyOwner
    {
        bytes32 codeName = keccak256(abi.encodePacked(code, name));

        if (rank == 0) {
            juniorPigeon[codeName] = pigeon;
            treasury[codeName] = msg.value;
            juniorPigeon[codeName] = pigeon;
            isPigeon[pigeon] = true;
            codeToName[code][name] = true;
        }

        if (rank == 1) {
            associatePigeon[codeName] = pigeon;
            treasury[codeName] = msg.value;
            associatePigeon[codeName] = pigeon;
            isPigeon[pigeon] = true;
            codeToName[code][name] = true;
        }

        if (rank == 2) {
            seniorPigeon[codeName] = pigeon;
            treasury[codeName] = msg.value;
            seniorPigeon[codeName] = pigeon;
            isPigeon[pigeon] = true;
            codeToName[code][name] = true;
        }
    }

    function exit() public onlyOwner {
        (bool success,) = owner.call{value: ownerBalance}("");
        require(success, "Transfer failed.");
    }
}
