// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "../lib/openzeppelin-contracts/contracts/access/Ownable.sol";
import "../lib/openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";
import "../lib/openzeppelin-contracts/contracts/token/ERC721/ERC721.sol";

interface AirdropLike {
    function airdropETH(address[] calldata, uint256[] calldata) external payable;
    function airdropERC20(address, address[] calldata, uint256[] calldata, uint256) external;
    function airdropERC721(address, address[] calldata, uint256[] calldata) external;
}

contract ChallengeERC20 is Ownable, ERC20 {
    constructor() ERC20("Challenge Token", "CT") Ownable(msg.sender) {}

    function mint(uint256 amount) external onlyOwner {
        _mint(msg.sender, amount);
    }
}

contract ChallengeERC721 is Ownable, ERC721 {
    constructor() ERC721("Challenge NFT", "CNFT") Ownable(msg.sender) {}

    function mint(uint256 id) external onlyOwner {
        _mint(msg.sender, id);
    }
}

contract Challenge {
    function randomAddress(uint256 seed) private view returns (uint256, address) {
        bytes32 v = keccak256(abi.encodePacked((seed >> 128) | (seed << 128)));
        return (uint256(keccak256(abi.encodePacked(seed))), address(bytes20(v)));
    }

    function randomUint(uint256 seed, uint256 min, uint256 max) private view returns (uint256, uint256) {
        bytes32 v = keccak256(abi.encodePacked((seed >> 128) | (seed << 128)));
        return (uint256(keccak256(abi.encodePacked(seed))), uint256(v) % (max - min) + min);
    }

    ChallengeERC20 private immutable CHALLENGE_TOKEN = new ChallengeERC20();
    ChallengeERC721 private immutable CHALLENGE_NFT = new ChallengeERC721();

    uint256 public bestScore = type(uint256).max;
    bytes public bestImplementation;

    function deposit() external payable {}

    function submit(AirdropLike dropper) external payable returns (uint256) {
        bytes memory implementation = address(dropper).code;

        uint256 gasUsed = 0;

        uint256 seed = uint256(blockhash(block.number - 1));

        address[] memory recipients = new address[](16);
        uint256[] memory amounts = new uint[](16);

        uint256 totalEth;
        for (uint256 i = 0; i < 16; i++) {
            (seed, recipients[i]) = randomAddress(seed);
            (seed, amounts[i]) = randomUint(seed, 1 ether, 5 ether);

            require(recipients[i].balance == 0, "unlucky");

            totalEth += amounts[i];
        }

        {
            uint256 start = gasleft();
            dropper.airdropETH{value: totalEth}(recipients, amounts);
            uint256 end = gasleft();

            for (uint256 i = 0; i < 16; i++) {
                require(recipients[i].balance == amounts[i], "failed to airdrop eth");
            }

            gasUsed += (start - end);
        }

        uint256 totalTokens;
        for (uint256 i = 0; i < 16; i++) {
            (seed, recipients[i]) = randomAddress(seed);
            (seed, amounts[i]) = randomUint(seed, 1 ether, 5 ether);

            require(CHALLENGE_TOKEN.balanceOf(recipients[i]) == 0, "unlucky");

            totalTokens += amounts[i];
        }

        CHALLENGE_TOKEN.approve(address(dropper), totalTokens);
        CHALLENGE_TOKEN.mint(totalTokens);

        {
            uint256 start = gasleft();
            dropper.airdropERC20(address(CHALLENGE_TOKEN), recipients, amounts, totalTokens);
            uint256 end = gasleft();

            for (uint256 i = 0; i < 16; i++) {
                require(CHALLENGE_TOKEN.balanceOf(recipients[i]) == amounts[i], "failed to airdrop token");
            }

            gasUsed += (start - end);
        }

        uint256 startId;
        (seed, startId) = randomUint(seed, 0, type(uint256).max);
        for (uint256 i = 0; i < 16; i++) {
            (seed, recipients[i]) = randomAddress(seed);
            amounts[i] = startId++;

            require(CHALLENGE_NFT.balanceOf(recipients[i]) == 0, "unlucky");
            CHALLENGE_NFT.mint(amounts[i]);
        }

        CHALLENGE_NFT.setApprovalForAll(address(dropper), true);

        {
            uint256 start = gasleft();
            dropper.airdropERC721(address(CHALLENGE_NFT), recipients, amounts);
            uint256 end = gasleft();

            for (uint256 i = 0; i < 16; i++) {
                require(CHALLENGE_NFT.ownerOf(amounts[i]) == recipients[i], "failed to airdrop nft");
            }

            gasUsed += (start - end);
        }

        CHALLENGE_NFT.setApprovalForAll(address(dropper), false);

        if (gasUsed < bestScore) {
            bestScore = gasUsed;
            bestImplementation = implementation;
        }

        return gasUsed;
    }

    function getScore() external view returns (uint256) {
        return bestScore;
    }
}
