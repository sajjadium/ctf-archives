import { expect } from "chai";
import { ethers } from "hardhat";
import { ChallengeToken } from "../typechain";


// This "Challenge Setup" block must be left as-is
describe("Challenge Setup", function () {
  it("Should deploy ChallengeToken", async function () {
    const ChallengeTokenFactory = await ethers.getContractFactory("ChallengeToken", (await ethers.getSigners()).pop());
    const challengeToken = await ChallengeTokenFactory.deploy();
    await challengeToken.deployed();
  });
});

// Try to solve the challenge below this line
// Run `npx hardhat ctf-try` to test your solution locally
// Run `npx hardhat ctf-try --submit` to submit your solution to the remote CTF node and get the real flag
describe("Solve Challenge", function () {
  let challengeToken: ChallengeToken;

  it("Should return the winning flag", async function () {
    challengeToken = await ethers.getContractAt("ChallengeToken", "0x73511669fd4dE447feD18BB79bAFeAC93aB7F31f");

    const returnedFlag = await challengeToken.did_i_win()

    console.log(`\tThe returned flag is: "${returnedFlag}"`)
  });
});
