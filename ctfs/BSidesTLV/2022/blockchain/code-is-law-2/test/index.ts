import { expect } from "chai";
import { Contract } from "ethers";
import { ethers } from "hardhat";

describe("ChallengeToken", function () {
  let challengeToken: Contract;
  let onlyICanHazToken: Contract;

  it("Should deploy contracts succesfully", async function () {
    const ChallengeToken = await ethers.getContractFactory("ChallengeToken");
    challengeToken = await ChallengeToken.deploy();
    await challengeToken.deployed();

    const OnlyICanHazToken = await ethers.getContractFactory("OnlyICanHazToken");
    onlyICanHazToken = await OnlyICanHazToken.deploy();
    await onlyICanHazToken.deployed();
  });


  it("Should send OnlyICanHazToken a token", async function () {
    expect(await challengeToken.balanceOf(onlyICanHazToken.address)).to.equal(0);
    await challengeToken.can_i_haz_token(onlyICanHazToken.address);
    expect(await challengeToken.balanceOf(onlyICanHazToken.address)).to.equal(1);
  });

  it("Should fail to send an EOA a token", async function () {
    const [EOA] = await ethers.getSigners();

    expect(await challengeToken.balanceOf(EOA.address)).to.equal(0);
    await expect(challengeToken.can_i_haz_token(EOA.address)).to.revertedWith("receiver is ineligible for a token because their codehash does not match the specific contract codehash required");
    expect(await challengeToken.balanceOf(EOA.address)).to.equal(0);
  });
});
