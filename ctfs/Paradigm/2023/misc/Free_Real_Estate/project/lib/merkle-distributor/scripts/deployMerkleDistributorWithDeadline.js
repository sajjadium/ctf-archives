require('dotenv').config()
require('@nomiclabs/hardhat-ethers')
const { ethers } = require('hardhat')

async function main() {
  const MerkleDistributorWithDeadline = await ethers.getContractFactory('MerkleDistributorWithDeadline')
  const merkleDistributorWithDeadline = await MerkleDistributorWithDeadline.deploy(
    // USDC
    '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
    '0xbe154afea9ba1e08729654a19c53952a892d6b37fe0b5d1bdf8ac4f51d03a426',
    1688493524
  )
  await merkleDistributorWithDeadline.deployed()
  console.log(`merkleDistributorWithDeadline deployed at ${merkleDistributorWithDeadline.address}`)
}

main()
  // eslint-disable-next-line no-process-exit
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error)
    // eslint-disable-next-line no-process-exit
    process.exit(1)
  })
