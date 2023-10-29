import { Fixture } from 'ethereum-waffle'
import { constants, Wallet } from 'ethers'
import { ethers, waffle } from 'hardhat'
import { MockTimeNonfungiblePositionManager, QuoterV2, TestERC20 } from '../typechain'
import completeFixture from './shared/completeFixture'
import { FeeAmount, MaxUint128 } from './shared/constants'
import { encodePriceSqrt } from './shared/encodePriceSqrt'
import { expandTo18Decimals } from './shared/expandTo18Decimals'
import { expect } from './shared/expect'
import { encodePath } from './shared/path'
import { createPool, createPoolWithMultiplePositions, createPoolWithZeroTickInitialized } from './shared/quoter'
import snapshotGasCost from './shared/snapshotGasCost'

describe('QuoterV2', function () {
  this.timeout(40000)
  let wallet: Wallet
  let trader: Wallet

  const swapRouterFixture: Fixture<{
    nft: MockTimeNonfungiblePositionManager
    tokens: [TestERC20, TestERC20, TestERC20]
    quoter: QuoterV2
  }> = async (wallets, provider) => {
    const { weth9, factory, router, tokens, nft } = await completeFixture(wallets, provider)

    // approve & fund wallets
    for (const token of tokens) {
      await token.approve(router.address, constants.MaxUint256)
      await token.approve(nft.address, constants.MaxUint256)
      await token.connect(trader).approve(router.address, constants.MaxUint256)
      await token.transfer(trader.address, expandTo18Decimals(1_000_000))
    }

    const quoterFactory = await ethers.getContractFactory('QuoterV2')
    quoter = (await quoterFactory.deploy(factory.address, weth9.address)) as QuoterV2

    return {
      tokens,
      nft,
      quoter,
    }
  }

  let nft: MockTimeNonfungiblePositionManager
  let tokens: [TestERC20, TestERC20, TestERC20]
  let quoter: QuoterV2

  let loadFixture: ReturnType<typeof waffle.createFixtureLoader>

  before('create fixture loader', async () => {
    const wallets = await (ethers as any).getSigners()
    ;[wallet, trader] = wallets
    loadFixture = waffle.createFixtureLoader(wallets)
  })

  // helper for getting weth and token balances
  beforeEach('load fixture', async () => {
    ;({ tokens, nft, quoter } = await loadFixture(swapRouterFixture))
  })

  describe('quotes', () => {
    beforeEach(async () => {
      await createPool(nft, wallet, tokens[0].address, tokens[1].address)
      await createPool(nft, wallet, tokens[1].address, tokens[2].address)
      await createPoolWithMultiplePositions(nft, wallet, tokens[0].address, tokens[2].address)
    })

    describe('#quoteExactInput', () => {
      it('0 -> 2 cross 2 tick', async () => {
        const {
          amountOut,
          sqrtPriceX96AfterList,
          initializedTicksCrossedList,
          gasEstimate,
        } = await quoter.callStatic.quoteExactInput(
          encodePath([tokens[0].address, tokens[2].address], [FeeAmount.MEDIUM]),
          10000
        )

        await snapshotGasCost(gasEstimate)
        expect(sqrtPriceX96AfterList.length).to.eq(1)
        expect(sqrtPriceX96AfterList[0]).to.eq('78461846509168490764501028180')
        expect(initializedTicksCrossedList[0]).to.eq(2)
        expect(amountOut).to.eq(9871)
      })

      it('0 -> 2 cross 2 tick where after is initialized', async () => {
        // The swap amount is set such that the active tick after the swap is -120.
        // -120 is an initialized tick for this pool. We check that we don't count it.
        const {
          amountOut,
          sqrtPriceX96AfterList,
          initializedTicksCrossedList,
          gasEstimate,
        } = await quoter.callStatic.quoteExactInput(
          encodePath([tokens[0].address, tokens[2].address], [FeeAmount.MEDIUM]),
          6200
        )

        await snapshotGasCost(gasEstimate)
        expect(sqrtPriceX96AfterList.length).to.eq(1)
        expect(sqrtPriceX96AfterList[0]).to.eq('78757224507315167622282810783')
        expect(initializedTicksCrossedList.length).to.eq(1)
        expect(initializedTicksCrossedList[0]).to.eq(1)
        expect(amountOut).to.eq(6143)
      })

      it('0 -> 2 cross 1 tick', async () => {
        const {
          amountOut,
          sqrtPriceX96AfterList,
          initializedTicksCrossedList,
          gasEstimate,
        } = await quoter.callStatic.quoteExactInput(
          encodePath([tokens[0].address, tokens[2].address], [FeeAmount.MEDIUM]),
          4000
        )

        await snapshotGasCost(gasEstimate)
        expect(initializedTicksCrossedList[0]).to.eq(1)
        expect(sqrtPriceX96AfterList.length).to.eq(1)
        expect(sqrtPriceX96AfterList[0]).to.eq('78926452400586371254602774705')
        expect(amountOut).to.eq(3971)
      })

      it('0 -> 2 cross 0 tick, starting tick not initialized', async () => {
        // Tick before 0, tick after -1.
        const {
          amountOut,
          sqrtPriceX96AfterList,
          initializedTicksCrossedList,
          gasEstimate,
        } = await quoter.callStatic.quoteExactInput(
          encodePath([tokens[0].address, tokens[2].address], [FeeAmount.MEDIUM]),
          10
        )

        await snapshotGasCost(gasEstimate)
        expect(initializedTicksCrossedList[0]).to.eq(0)
        expect(sqrtPriceX96AfterList.length).to.eq(1)
        expect(sqrtPriceX96AfterList[0]).to.eq('79227483487511329217250071027')
        expect(amountOut).to.eq(8)
      })

      it('0 -> 2 cross 0 tick, starting tick initialized', async () => {
        // Tick before 0, tick after -1. Tick 0 initialized.
        await createPoolWithZeroTickInitialized(nft, wallet, tokens[0].address, tokens[2].address)

        const {
          amountOut,
          sqrtPriceX96AfterList,
          initializedTicksCrossedList,
          gasEstimate,
        } = await quoter.callStatic.quoteExactInput(
          encodePath([tokens[0].address, tokens[2].address], [FeeAmount.MEDIUM]),
          10
        )

        await snapshotGasCost(gasEstimate)
        expect(initializedTicksCrossedList[0]).to.eq(1)
        expect(sqrtPriceX96AfterList.length).to.eq(1)
        expect(sqrtPriceX96AfterList[0]).to.eq('79227817515327498931091950511')
        expect(amountOut).to.eq(8)
      })

      it('2 -> 0 cross 2', async () => {
        const {
          amountOut,
          sqrtPriceX96AfterList,
          initializedTicksCrossedList,
          gasEstimate,
        } = await quoter.callStatic.quoteExactInput(
          encodePath([tokens[2].address, tokens[0].address], [FeeAmount.MEDIUM]),
          10000
        )

        await snapshotGasCost(gasEstimate)
        expect(initializedTicksCrossedList[0]).to.eq(2)
        expect(sqrtPriceX96AfterList.length).to.eq(1)
        expect(sqrtPriceX96AfterList[0]).to.eq('80001962924147897865541384515')
        expect(initializedTicksCrossedList.length).to.eq(1)
        expect(amountOut).to.eq(9871)
      })

      it('2 -> 0 cross 2 where tick after is initialized', async () => {
        // The swap amount is set such that the active tick after the swap is 120.
        // 120 is an initialized tick for this pool. We check we don't count it.
        const {
          amountOut,
          sqrtPriceX96AfterList,
          initializedTicksCrossedList,
          gasEstimate,
        } = await quoter.callStatic.quoteExactInput(
          encodePath([tokens[2].address, tokens[0].address], [FeeAmount.MEDIUM]),
          6250
        )

        await snapshotGasCost(gasEstimate)
        expect(initializedTicksCrossedList[0]).to.eq(2)
        expect(sqrtPriceX96AfterList.length).to.eq(1)
        expect(sqrtPriceX96AfterList[0]).to.eq('79705728824507063507279123685')
        expect(initializedTicksCrossedList.length).to.eq(1)
        expect(amountOut).to.eq(6190)
      })

      it('2 -> 0 cross 0 tick, starting tick initialized', async () => {
        // Tick 0 initialized. Tick after = 1
        await createPoolWithZeroTickInitialized(nft, wallet, tokens[0].address, tokens[2].address)

        const {
          amountOut,
          sqrtPriceX96AfterList,
          initializedTicksCrossedList,
          gasEstimate,
        } = await quoter.callStatic.quoteExactInput(
          encodePath([tokens[2].address, tokens[0].address], [FeeAmount.MEDIUM]),
          200
        )

        await snapshotGasCost(gasEstimate)
        expect(initializedTicksCrossedList[0]).to.eq(0)
        expect(sqrtPriceX96AfterList.length).to.eq(1)
        expect(sqrtPriceX96AfterList[0]).to.eq('79235729830182478001034429156')
        expect(initializedTicksCrossedList.length).to.eq(1)
        expect(amountOut).to.eq(198)
      })

      it('2 -> 0 cross 0 tick, starting tick not initialized', async () => {
        // Tick 0 initialized. Tick after = 1
        const {
          amountOut,
          sqrtPriceX96AfterList,
          initializedTicksCrossedList,
          gasEstimate,
        } = await quoter.callStatic.quoteExactInput(
          encodePath([tokens[2].address, tokens[0].address], [FeeAmount.MEDIUM]),
          103
        )

        await snapshotGasCost(gasEstimate)
        expect(initializedTicksCrossedList[0]).to.eq(0)
        expect(sqrtPriceX96AfterList.length).to.eq(1)
        expect(sqrtPriceX96AfterList[0]).to.eq('79235858216754624215638319723')
        expect(initializedTicksCrossedList.length).to.eq(1)
        expect(amountOut).to.eq(101)
      })

      it('2 -> 1', async () => {
        const {
          amountOut,
          sqrtPriceX96AfterList,
          initializedTicksCrossedList,
          gasEstimate,
        } = await quoter.callStatic.quoteExactInput(
          encodePath([tokens[2].address, tokens[1].address], [FeeAmount.MEDIUM]),
          10000
        )

        await snapshotGasCost(gasEstimate)
        expect(sqrtPriceX96AfterList.length).to.eq(1)
        expect(sqrtPriceX96AfterList[0]).to.eq('80018067294531553039351583520')
        expect(initializedTicksCrossedList[0]).to.eq(0)
        expect(amountOut).to.eq(9871)
      })

      it('0 -> 2 -> 1', async () => {
        const {
          amountOut,
          sqrtPriceX96AfterList,
          initializedTicksCrossedList,
          gasEstimate,
        } = await quoter.callStatic.quoteExactInput(
          encodePath([tokens[0].address, tokens[2].address, tokens[1].address], [FeeAmount.MEDIUM, FeeAmount.MEDIUM]),
          10000
        )

        await snapshotGasCost(gasEstimate)
        expect(sqrtPriceX96AfterList.length).to.eq(2)
        expect(sqrtPriceX96AfterList[0]).to.eq('78461846509168490764501028180')
        expect(sqrtPriceX96AfterList[1]).to.eq('80007846861567212939802016351')
        expect(initializedTicksCrossedList[0]).to.eq(2)
        expect(initializedTicksCrossedList[1]).to.eq(0)
        expect(amountOut).to.eq(9745)
      })
    })

    describe('#quoteExactInputSingle', () => {
      it('0 -> 2', async () => {
        const {
          amountOut: quote,
          sqrtPriceX96After,
          initializedTicksCrossed,
          gasEstimate,
        } = await quoter.callStatic.quoteExactInputSingle({
          tokenIn: tokens[0].address,
          tokenOut: tokens[2].address,
          fee: FeeAmount.MEDIUM,
          amountIn: 10000,
          // -2%
          sqrtPriceLimitX96: encodePriceSqrt(100, 102),
        })

        await snapshotGasCost(gasEstimate)
        expect(initializedTicksCrossed).to.eq(2)
        expect(quote).to.eq(9871)
        expect(sqrtPriceX96After).to.eq('78461846509168490764501028180')
      })

      it('2 -> 0', async () => {
        const {
          amountOut: quote,
          sqrtPriceX96After,
          initializedTicksCrossed,
          gasEstimate,
        } = await quoter.callStatic.quoteExactInputSingle({
          tokenIn: tokens[2].address,
          tokenOut: tokens[0].address,
          fee: FeeAmount.MEDIUM,
          amountIn: 10000,
          // +2%
          sqrtPriceLimitX96: encodePriceSqrt(102, 100),
        })

        await snapshotGasCost(gasEstimate)
        expect(initializedTicksCrossed).to.eq(2)
        expect(quote).to.eq(9871)
        expect(sqrtPriceX96After).to.eq('80001962924147897865541384515')
      })
    })

    describe('#quoteExactOutput', () => {
      it('0 -> 2 cross 2 tick', async () => {
        const {
          amountIn,
          sqrtPriceX96AfterList,
          initializedTicksCrossedList,
          gasEstimate,
        } = await quoter.callStatic.quoteExactOutput(
          encodePath([tokens[2].address, tokens[0].address], [FeeAmount.MEDIUM]),
          15000
        )

        await snapshotGasCost(gasEstimate)
        expect(initializedTicksCrossedList.length).to.eq(1)
        expect(initializedTicksCrossedList[0]).to.eq(2)
        expect(amountIn).to.eq(15273)

        expect(sqrtPriceX96AfterList.length).to.eq(1)
        expect(sqrtPriceX96AfterList[0]).to.eq('78055527257643669242286029831')
      })

      it('0 -> 2 cross 2 where tick after is initialized', async () => {
        // The swap amount is set such that the active tick after the swap is -120.
        // -120 is an initialized tick for this pool. We check that we count it.
        const {
          amountIn,
          sqrtPriceX96AfterList,
          initializedTicksCrossedList,
          gasEstimate,
        } = await quoter.callStatic.quoteExactOutput(
          encodePath([tokens[2].address, tokens[0].address], [FeeAmount.MEDIUM]),
          6143
        )

        await snapshotGasCost(gasEstimate)
        expect(sqrtPriceX96AfterList.length).to.eq(1)
        expect(sqrtPriceX96AfterList[0]).to.eq('78757225449310403327341205211')
        expect(initializedTicksCrossedList.length).to.eq(1)
        expect(initializedTicksCrossedList[0]).to.eq(1)
        expect(amountIn).to.eq(6200)
      })

      it('0 -> 2 cross 1 tick', async () => {
        const {
          amountIn,
          sqrtPriceX96AfterList,
          initializedTicksCrossedList,
          gasEstimate,
        } = await quoter.callStatic.quoteExactOutput(
          encodePath([tokens[2].address, tokens[0].address], [FeeAmount.MEDIUM]),
          4000
        )

        await snapshotGasCost(gasEstimate)
        expect(initializedTicksCrossedList.length).to.eq(1)
        expect(initializedTicksCrossedList[0]).to.eq(1)
        expect(amountIn).to.eq(4029)

        expect(sqrtPriceX96AfterList.length).to.eq(1)
        expect(sqrtPriceX96AfterList[0]).to.eq('78924219757724709840818372098')
      })

      it('0 -> 2 cross 0 tick starting tick initialized', async () => {
        // Tick before 0, tick after 1. Tick 0 initialized.
        await createPoolWithZeroTickInitialized(nft, wallet, tokens[0].address, tokens[2].address)
        const {
          amountIn,
          sqrtPriceX96AfterList,
          initializedTicksCrossedList,
          gasEstimate,
        } = await quoter.callStatic.quoteExactOutput(
          encodePath([tokens[2].address, tokens[0].address], [FeeAmount.MEDIUM]),
          100
        )

        await snapshotGasCost(gasEstimate)
        expect(initializedTicksCrossedList.length).to.eq(1)
        expect(initializedTicksCrossedList[0]).to.eq(1)
        expect(amountIn).to.eq(102)

        expect(sqrtPriceX96AfterList.length).to.eq(1)
        expect(sqrtPriceX96AfterList[0]).to.eq('79224329176051641448521403903')
      })

      it('0 -> 2 cross 0 tick starting tick not initialized', async () => {
        const {
          amountIn,
          sqrtPriceX96AfterList,
          initializedTicksCrossedList,
          gasEstimate,
        } = await quoter.callStatic.quoteExactOutput(
          encodePath([tokens[2].address, tokens[0].address], [FeeAmount.MEDIUM]),
          10
        )

        await snapshotGasCost(gasEstimate)
        expect(initializedTicksCrossedList.length).to.eq(1)
        expect(initializedTicksCrossedList[0]).to.eq(0)
        expect(amountIn).to.eq(12)

        expect(sqrtPriceX96AfterList.length).to.eq(1)
        expect(sqrtPriceX96AfterList[0]).to.eq('79227408033628034983534698435')
      })

      it('2 -> 0 cross 2 ticks', async () => {
        const {
          amountIn,
          sqrtPriceX96AfterList,
          initializedTicksCrossedList,
          gasEstimate,
        } = await quoter.callStatic.quoteExactOutput(
          encodePath([tokens[0].address, tokens[2].address], [FeeAmount.MEDIUM]),
          15000
        )

        await snapshotGasCost(gasEstimate)
        expect(initializedTicksCrossedList.length).to.eq(1)
        expect(initializedTicksCrossedList[0]).to.eq(2)
        expect(amountIn).to.eq(15273)
        expect(sqrtPriceX96AfterList.length).to.eq(1)
        expect(sqrtPriceX96AfterList[0]).to.eq('80418414376567919517220409857')
      })

      it('2 -> 0 cross 2 where tick after is initialized', async () => {
        // The swap amount is set such that the active tick after the swap is 120.
        // 120 is an initialized tick for this pool. We check that we don't count it.
        const {
          amountIn,
          sqrtPriceX96AfterList,
          initializedTicksCrossedList,
          gasEstimate,
        } = await quoter.callStatic.quoteExactOutput(
          encodePath([tokens[0].address, tokens[2].address], [FeeAmount.MEDIUM]),
          6223
        )

        await snapshotGasCost(gasEstimate)
        expect(initializedTicksCrossedList[0]).to.eq(2)
        expect(sqrtPriceX96AfterList.length).to.eq(1)
        expect(sqrtPriceX96AfterList[0]).to.eq('79708304437530892332449657932')
        expect(initializedTicksCrossedList.length).to.eq(1)
        expect(amountIn).to.eq(6283)
      })

      it('2 -> 0 cross 1 tick', async () => {
        const {
          amountIn,
          sqrtPriceX96AfterList,
          initializedTicksCrossedList,
          gasEstimate,
        } = await quoter.callStatic.quoteExactOutput(
          encodePath([tokens[0].address, tokens[2].address], [FeeAmount.MEDIUM]),
          6000
        )

        await snapshotGasCost(gasEstimate)
        expect(initializedTicksCrossedList[0]).to.eq(1)
        expect(sqrtPriceX96AfterList.length).to.eq(1)
        expect(sqrtPriceX96AfterList[0]).to.eq('79690640184021170956740081887')
        expect(initializedTicksCrossedList.length).to.eq(1)
        expect(amountIn).to.eq(6055)
      })

      it('2 -> 1', async () => {
        const {
          amountIn,
          sqrtPriceX96AfterList,
          initializedTicksCrossedList,
          gasEstimate,
        } = await quoter.callStatic.quoteExactOutput(
          encodePath([tokens[1].address, tokens[2].address], [FeeAmount.MEDIUM]),
          9871
        )

        await snapshotGasCost(gasEstimate)
        expect(sqrtPriceX96AfterList.length).to.eq(1)
        expect(sqrtPriceX96AfterList[0]).to.eq('80018020393569259756601362385')
        expect(initializedTicksCrossedList[0]).to.eq(0)
        expect(amountIn).to.eq(10000)
      })

      it('0 -> 2 -> 1', async () => {
        const {
          amountIn,
          sqrtPriceX96AfterList,
          initializedTicksCrossedList,
          gasEstimate,
        } = await quoter.callStatic.quoteExactOutput(
          encodePath([tokens[0].address, tokens[2].address, tokens[1].address].reverse(), [
            FeeAmount.MEDIUM,
            FeeAmount.MEDIUM,
          ]),
          9745
        )

        await snapshotGasCost(gasEstimate)
        expect(sqrtPriceX96AfterList.length).to.eq(2)
        expect(sqrtPriceX96AfterList[0]).to.eq('80007838904387594703933785072')
        expect(sqrtPriceX96AfterList[1]).to.eq('78461888503179331029803316753')
        expect(initializedTicksCrossedList[0]).to.eq(0)
        expect(initializedTicksCrossedList[1]).to.eq(2)
        expect(amountIn).to.eq(10000)
      })
    })

    describe('#quoteExactOutputSingle', () => {
      it('0 -> 1', async () => {
        const {
          amountIn,
          sqrtPriceX96After,
          initializedTicksCrossed,
          gasEstimate,
        } = await quoter.callStatic.quoteExactOutputSingle({
          tokenIn: tokens[0].address,
          tokenOut: tokens[1].address,
          fee: FeeAmount.MEDIUM,
          amount: MaxUint128,
          sqrtPriceLimitX96: encodePriceSqrt(100, 102),
        })

        await snapshotGasCost(gasEstimate)
        expect(amountIn).to.eq(9981)
        expect(initializedTicksCrossed).to.eq(0)
        expect(sqrtPriceX96After).to.eq('78447570448055484695608110440')
      })

      it('1 -> 0', async () => {
        const {
          amountIn,
          sqrtPriceX96After,
          initializedTicksCrossed,
          gasEstimate,
        } = await quoter.callStatic.quoteExactOutputSingle({
          tokenIn: tokens[1].address,
          tokenOut: tokens[0].address,
          fee: FeeAmount.MEDIUM,
          amount: MaxUint128,
          sqrtPriceLimitX96: encodePriceSqrt(102, 100),
        })

        await snapshotGasCost(gasEstimate)
        expect(amountIn).to.eq(9981)
        expect(initializedTicksCrossed).to.eq(0)
        expect(sqrtPriceX96After).to.eq('80016521857016594389520272648')
      })
    })
  })
})
