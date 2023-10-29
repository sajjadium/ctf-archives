import { Contract, constants, Wallet } from 'ethers'
import { waffle, ethers } from 'hardhat'
import { Fixture } from 'ethereum-waffle'
import completeFixture from './shared/completeFixture'
import { expect } from './shared/expect'
import { TestERC20, TestCallbackValidation } from '../typechain'
import { FeeAmount } from './shared/constants'

describe('CallbackValidation', () => {
  let nonpairAddr: Wallet, wallets: Wallet[]

  const callbackValidationFixture: Fixture<{
    callbackValidation: TestCallbackValidation
    tokens: [TestERC20, TestERC20]
    factory: Contract
  }> = async (wallets, provider) => {
    const { factory } = await completeFixture(wallets, provider)
    const tokenFactory = await ethers.getContractFactory('TestERC20')
    const callbackValidationFactory = await ethers.getContractFactory('TestCallbackValidation')
    const tokens: [TestERC20, TestERC20] = [
      (await tokenFactory.deploy(constants.MaxUint256.div(2))) as TestERC20, // do not use maxu256 to avoid overflowing
      (await tokenFactory.deploy(constants.MaxUint256.div(2))) as TestERC20,
    ]
    const callbackValidation = (await callbackValidationFactory.deploy()) as TestCallbackValidation

    return {
      tokens,
      callbackValidation,
      factory,
    }
  }

  let callbackValidation: TestCallbackValidation
  let tokens: [TestERC20, TestERC20]
  let factory: Contract

  let loadFixture: ReturnType<typeof waffle.createFixtureLoader>

  before('create fixture loader', async () => {
    ;[nonpairAddr, ...wallets] = await (ethers as any).getSigners()

    loadFixture = waffle.createFixtureLoader(wallets)
  })

  beforeEach('load fixture', async () => {
    ;({ callbackValidation, tokens, factory } = await loadFixture(callbackValidationFixture))
  })

  it('reverts when called from an address other than the associated UniswapV3Pool', async () => {
    expect(
      callbackValidation
        .connect(nonpairAddr)
        .verifyCallback(factory.address, tokens[0].address, tokens[1].address, FeeAmount.MEDIUM)
    ).to.be.reverted
  })
})
