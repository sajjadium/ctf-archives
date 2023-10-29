import { waffle, ethers, artifacts } from 'hardhat'

import { expect } from './shared/expect'

import { PoolTicksCounterTest } from '../typechain'
import { deployMockContract, Fixture, MockContract } from 'ethereum-waffle'
import { Artifact } from 'hardhat/types'

describe('PoolTicksCounter', () => {
  const TICK_SPACINGS = [200, 60, 10]

  TICK_SPACINGS.forEach((TICK_SPACING) => {
    let PoolTicksCounter: PoolTicksCounterTest
    let pool: MockContract
    let PoolAbi: Artifact

    // Bit index to tick
    const bitIdxToTick = (idx: number, page = 0) => {
      return idx * TICK_SPACING + page * 256 * TICK_SPACING
    }

    before(async () => {
      const wallets = await (ethers as any).getSigners()
      PoolAbi = await artifacts.readArtifact('IUniswapV3Pool')
      const poolTicksHelperFactory = await ethers.getContractFactory('PoolTicksCounterTest')
      PoolTicksCounter = (await poolTicksHelperFactory.deploy()) as PoolTicksCounterTest
      pool = await deployMockContract(wallets[0], PoolAbi.abi)
      await pool.mock.tickSpacing.returns(TICK_SPACING)
    })

    describe(`[Tick Spacing: ${TICK_SPACING}]: tick after is bigger`, async () => {
      it('same tick initialized', async () => {
        await pool.mock.tickBitmap.withArgs(0).returns(0b1100) // 1100
        const result = await PoolTicksCounter.countInitializedTicksCrossed(
          pool.address,
          bitIdxToTick(2),
          bitIdxToTick(2)
        )
        expect(result).to.be.eq(1)
      })

      it('same tick not-initialized', async () => {
        await pool.mock.tickBitmap.withArgs(0).returns(0b1100) // 1100
        const result = await PoolTicksCounter.countInitializedTicksCrossed(
          pool.address,
          bitIdxToTick(1),
          bitIdxToTick(1)
        )
        expect(result).to.be.eq(0)
      })

      it('same page', async () => {
        await pool.mock.tickBitmap.withArgs(0).returns(0b1100) // 1100
        const result = await PoolTicksCounter.countInitializedTicksCrossed(
          pool.address,
          bitIdxToTick(0),
          bitIdxToTick(255)
        )
        expect(result).to.be.eq(2)
      })

      it('multiple pages', async () => {
        await pool.mock.tickBitmap.withArgs(0).returns(0b1100) // 1100
        await pool.mock.tickBitmap.withArgs(1).returns(0b1101) // 1101
        const result = await PoolTicksCounter.countInitializedTicksCrossed(
          pool.address,
          bitIdxToTick(0),
          bitIdxToTick(255, 1)
        )
        expect(result).to.be.eq(5)
      })

      it('counts all ticks in a page except ending tick', async () => {
        await pool.mock.tickBitmap.withArgs(0).returns(ethers.constants.MaxUint256)
        await pool.mock.tickBitmap.withArgs(1).returns(0x0)
        const result = await PoolTicksCounter.countInitializedTicksCrossed(
          pool.address,
          bitIdxToTick(0),
          bitIdxToTick(255, 1)
        )
        expect(result).to.be.eq(255)
      })

      it('counts ticks to left of start and right of end on same page', async () => {
        await pool.mock.tickBitmap.withArgs(0).returns(0b1111000100001111)
        const result = await PoolTicksCounter.countInitializedTicksCrossed(
          pool.address,
          bitIdxToTick(8),
          bitIdxToTick(255)
        )
        expect(result).to.be.eq(4)
      })

      it('counts ticks to left of start and right of end across on multiple pages', async () => {
        await pool.mock.tickBitmap.withArgs(0).returns(0b1111000100001111)
        await pool.mock.tickBitmap.withArgs(1).returns(0b1111000100001111)
        const result = await PoolTicksCounter.countInitializedTicksCrossed(
          pool.address,
          bitIdxToTick(8),
          bitIdxToTick(8, 1)
        )
        expect(result).to.be.eq(9)
      })

      it('counts ticks when before and after are initialized on same page', async () => {
        await pool.mock.tickBitmap.withArgs(0).returns(0b11111100)
        const startingTickInit = await PoolTicksCounter.countInitializedTicksCrossed(
          pool.address,
          bitIdxToTick(2),
          bitIdxToTick(255)
        )
        expect(startingTickInit).to.be.eq(5)
        const endingTickInit = await PoolTicksCounter.countInitializedTicksCrossed(
          pool.address,
          bitIdxToTick(0),
          bitIdxToTick(3)
        )
        expect(endingTickInit).to.be.eq(2)
        const bothInit = await PoolTicksCounter.countInitializedTicksCrossed(
          pool.address,
          bitIdxToTick(2),
          bitIdxToTick(5)
        )
        expect(bothInit).to.be.eq(3)
      })

      it('counts ticks when before and after are initialized on multiple page', async () => {
        await pool.mock.tickBitmap.withArgs(0).returns(0b11111100)
        await pool.mock.tickBitmap.withArgs(1).returns(0b11111100)
        const startingTickInit = await PoolTicksCounter.countInitializedTicksCrossed(
          pool.address,
          bitIdxToTick(2),
          bitIdxToTick(255)
        )
        expect(startingTickInit).to.be.eq(5)
        const endingTickInit = await PoolTicksCounter.countInitializedTicksCrossed(
          pool.address,
          bitIdxToTick(0),
          bitIdxToTick(3, 1)
        )
        expect(endingTickInit).to.be.eq(8)
        const bothInit = await PoolTicksCounter.countInitializedTicksCrossed(
          pool.address,
          bitIdxToTick(2),
          bitIdxToTick(5, 1)
        )
        expect(bothInit).to.be.eq(9)
      })

      it('counts ticks with lots of pages', async () => {
        await pool.mock.tickBitmap.withArgs(0).returns(0b11111100)
        await pool.mock.tickBitmap.withArgs(1).returns(0b11111111)
        await pool.mock.tickBitmap.withArgs(2).returns(0x0)
        await pool.mock.tickBitmap.withArgs(3).returns(0x0)
        await pool.mock.tickBitmap.withArgs(4).returns(0b11111100)

        const bothInit = await PoolTicksCounter.countInitializedTicksCrossed(
          pool.address,
          bitIdxToTick(4),
          bitIdxToTick(5, 4)
        )
        expect(bothInit).to.be.eq(15)
      })
    })

    describe(`[Tick Spacing: ${TICK_SPACING}]: tick after is smaller`, async () => {
      it('same page', async () => {
        await pool.mock.tickBitmap.withArgs(0).returns(0b1100)
        const result = await PoolTicksCounter.countInitializedTicksCrossed(
          pool.address,
          bitIdxToTick(255),
          bitIdxToTick(0)
        )
        expect(result).to.be.eq(2)
      })

      it('multiple pages', async () => {
        await pool.mock.tickBitmap.withArgs(0).returns(0b1100)
        await pool.mock.tickBitmap.withArgs(-1).returns(0b1100)
        const result = await PoolTicksCounter.countInitializedTicksCrossed(
          pool.address,
          bitIdxToTick(255),
          bitIdxToTick(0, -1)
        )
        expect(result).to.be.eq(4)
      })

      it('counts all ticks in a page', async () => {
        await pool.mock.tickBitmap.withArgs(0).returns(ethers.constants.MaxUint256)
        await pool.mock.tickBitmap.withArgs(-1).returns(0x0)
        const result = await PoolTicksCounter.countInitializedTicksCrossed(
          pool.address,
          bitIdxToTick(255),
          bitIdxToTick(0, -1)
        )
        expect(result).to.be.eq(256)
      })

      it('counts ticks to right of start and left of end on same page', async () => {
        await pool.mock.tickBitmap.withArgs(0).returns(0b1111000100001111)
        const result = await PoolTicksCounter.countInitializedTicksCrossed(
          pool.address,
          bitIdxToTick(15),
          bitIdxToTick(2)
        )
        expect(result).to.be.eq(6)
      })

      it('counts ticks to right of start and left of end on multiple pages', async () => {
        await pool.mock.tickBitmap.withArgs(0).returns(0b1111000100001111)
        await pool.mock.tickBitmap.withArgs(-1).returns(0b1111000100001111)
        const result = await PoolTicksCounter.countInitializedTicksCrossed(
          pool.address,
          bitIdxToTick(8),
          bitIdxToTick(8, -1)
        )
        expect(result).to.be.eq(9)
      })

      it('counts ticks when before and after are initialized on same page', async () => {
        await pool.mock.tickBitmap.withArgs(0).returns(0b11111100)
        const startingTickInit = await PoolTicksCounter.countInitializedTicksCrossed(
          pool.address,
          bitIdxToTick(3),
          bitIdxToTick(0)
        )
        expect(startingTickInit).to.be.eq(2)
        const endingTickInit = await PoolTicksCounter.countInitializedTicksCrossed(
          pool.address,
          bitIdxToTick(255),
          bitIdxToTick(2)
        )
        expect(endingTickInit).to.be.eq(5)
        const bothInit = await PoolTicksCounter.countInitializedTicksCrossed(
          pool.address,
          bitIdxToTick(5),
          bitIdxToTick(2)
        )
        expect(bothInit).to.be.eq(3)
      })

      it('counts ticks when before and after are initialized on multiple page', async () => {
        await pool.mock.tickBitmap.withArgs(0).returns(0b11111100)
        await pool.mock.tickBitmap.withArgs(-1).returns(0b11111100)
        const startingTickInit = await PoolTicksCounter.countInitializedTicksCrossed(
          pool.address,
          bitIdxToTick(2),
          bitIdxToTick(3, -1)
        )
        expect(startingTickInit).to.be.eq(5)
        const endingTickInit = await PoolTicksCounter.countInitializedTicksCrossed(
          pool.address,
          bitIdxToTick(5),
          bitIdxToTick(255, -1)
        )
        expect(endingTickInit).to.be.eq(4)
        const bothInit = await PoolTicksCounter.countInitializedTicksCrossed(
          pool.address,
          bitIdxToTick(2),
          bitIdxToTick(5, -1)
        )
        expect(bothInit).to.be.eq(3)
      })

      it('counts ticks with lots of pages', async () => {
        await pool.mock.tickBitmap.withArgs(0).returns(0b11111100)
        await pool.mock.tickBitmap.withArgs(-1).returns(0xff)
        await pool.mock.tickBitmap.withArgs(-2).returns(0x0)
        await pool.mock.tickBitmap.withArgs(-3).returns(0x0)
        await pool.mock.tickBitmap.withArgs(-4).returns(0b11111100)
        const bothInit = await PoolTicksCounter.countInitializedTicksCrossed(
          pool.address,
          bitIdxToTick(3),
          bitIdxToTick(6, -4)
        )
        expect(bothInit).to.be.eq(11)
      })
    })
  })
})
