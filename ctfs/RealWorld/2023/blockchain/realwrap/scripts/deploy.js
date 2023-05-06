const { ethers } = require("hardhat");

async function main() {
  const amount = ethers.utils.parseEther("1");

  const Factory = await ethers.getContractFactory("Factory");
  const factory = await Factory.deploy({ value: amount, gasLimit: 6000000 });
  await factory.deployed();

  console.log(`Factory deployed to ${factory.address}`);
  console.log(`isSolved: ${await factory.isSolved()}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
