import { expect } from "chai";
import { Contract } from "ethers";
import { ethers } from "hardhat";
import { ChallengeToken, OnlyICanHazToken } from "../typechain";

describe("ChallengeToken Contract", function () {
    let challengeToken: ChallengeToken;
    let onlyICanHazToken: OnlyICanHazToken;

    it("Should deploy ChallengeToken succesfully", async function () {
        const signers = await ethers.getSigners();
        const ChallengeTokenFactory = await ethers.getContractFactory("ChallengeToken", signers.pop());
        challengeToken = await ChallengeTokenFactory.deploy();
        await challengeToken.deployed();
        challengeToken = challengeToken.connect(signers[0]);
        // console.log("\tChallengeToken succesfully deployed at\t\t", challengeToken.address);
    });

    it("Should deploy OnlyICanHazToken succesfully", async function () {
        const OnlyICanHazTokenFactory = await ethers.getContractFactory("OnlyICanHazToken");
        onlyICanHazToken = await OnlyICanHazTokenFactory.deploy();
        await onlyICanHazToken.deployed();
        // console.log("\tOnlyICanHazToken succesfully deployed at\t", onlyICanHazToken.address);
    });

    it("ChallengeToken should send OnlyICanHazToken a token", async function () {
        expect(await challengeToken.balanceOf(onlyICanHazToken.address)).to.equal(0);
        await challengeToken.can_i_haz_token(onlyICanHazToken.address);
        expect(await challengeToken.balanceOf(onlyICanHazToken.address)).to.equal(1);
    });

    it("Should deploy OnlyICanHazToken a second time", async function () {
        const OnlyICanHazTokenFactory = await ethers.getContractFactory("OnlyICanHazToken");
        onlyICanHazToken = await OnlyICanHazTokenFactory.deploy();
        await onlyICanHazToken.deployed();
        // console.log("\tOnlyICanHazToken succesfully deployed at\t", onlyICanHazToken.address);
    });

    it("ChallengeToken should fail to send a token to a OnlyICanHazToken contract that is not the first contract deployed by the transaction initiator", async function () {
        await expect(challengeToken.can_i_haz_token(onlyICanHazToken.address)).to.revertedWith("receiver is ineligible for a token because they are not the first contract deployed by the EOA who initiated this transaction");
    });

    it("ChallengeToken should not give a flag when msg.sender doesn't have a token", async function () {
        await expect(challengeToken.did_i_win()).to.revertedWith("you shall not pass");
    });
});
