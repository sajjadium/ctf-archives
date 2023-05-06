use anchor_lang::prelude::*;
use anchor_spl::token::{Mint, Token, TokenAccount, Transfer};
use anchor_spl::token;
use borsh::{BorshSerialize, BorshDeserialize};

pub use anchor_lang;
pub use anchor_spl;

pub const FLAG_SEED: &[u8] = b"flag";

declare_id!("osecio1111111111111111111111111111111111112");

type FLAG = bool;
type NUMBER = i64;
#[program]
pub mod chall {
    use super::*;

    pub fn init(ctx: Context<Init>) -> Result<()> {
        let state = &mut ctx.accounts.state.load_init()?;

        state.owner = Some(ctx.accounts.payer.key());

        Ok(())
    }
    
    pub fn init_virtual_balance(ctx: Context<Auth>, x: NUMBER, y: NUMBER) -> Result<()> {
        let state = &mut ctx.accounts.state.load_mut()?;

        state.x = x;
        state.y = y;

        Ok(())
    }
    
    pub fn set_enabled(ctx: Context<AuthFee>, enabled: FLAG) -> Result<()> {
        let state = &mut ctx.accounts.state.load_mut()?;

        state.enabled = enabled;

        Ok(())
    }
    
    pub fn set_fee_manager(ctx: Context<Auth>, manager: FeeManager) -> Result<()> {
        let state = &mut ctx.accounts.state.load_mut()?;

        state.fee_manager = Some(manager);

        Ok(())
    }
    
    pub fn set_owner(ctx: Context<Auth>, owner: Option<Pubkey>) -> Result<()> {
        let state = &mut ctx.accounts.state.load_mut()?;

        state.owner = owner;

        Ok(())
    }
    
    pub fn set_fee(ctx: Context<AuthFee>, fee: NUMBER) -> Result<()> {
        let state = &mut ctx.accounts.state.load_mut()?;

        state.fee = fee;

        Ok(())
    }
    
    pub fn swap(ctx: Context<Swap>, amt: NUMBER) -> Result<()> {
        let state = &mut ctx.accounts.state.load_mut()?;

        state.x += amt;
        state.y += amt;

        state.x += state.fee * state.x / 100;
        state.y += state.fee * state.y / 100;

        Ok(())
    }

}

#[derive(Accounts)]
pub struct Init<'info> {
    #[account(
        init,
        seeds = [ FLAG_SEED ],
        bump,
        payer = payer,
        space = 1000
    )]
    pub state: AccountLoader<'info, State>,

    #[account(mut)]
    pub payer: Signer<'info>,
    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,
}

#[derive(Accounts)]
pub struct Auth<'info> {
    #[account(mut,
        constraint = (state.load().unwrap().owner.is_some() && 
            state.load().unwrap().owner.unwrap() == payer.key()
        )
    )]
    pub state: AccountLoader<'info, State>,
    #[account(mut)]
    pub payer: Signer<'info>,
    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,
}

#[derive(Accounts)]
pub struct AuthFee<'info> {
    #[account(mut,
        constraint = (state.load().unwrap().owner.is_some() && 
            state.load().unwrap().owner.unwrap() == payer.key()
        ) || 
        (state.load().unwrap().fee_manager.is_some() && (
            state.load().unwrap().fee_manager.unwrap().timestamp < Clock::get()?.unix_timestamp && 
            (
                state.load().unwrap().fee_manager.unwrap().authority.is_none() || 
                state.load().unwrap().fee_manager.unwrap().authority.unwrap() == payer.key()
            )
        ))
    )]
    pub state: AccountLoader<'info, State>,
    #[account(mut)]
    pub payer: Signer<'info>,
    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,
}

#[derive(Accounts)]
pub struct Swap<'info> {
    #[account(mut,
        constraint = state.load().unwrap().enabled
    )]
    pub state: AccountLoader<'info, State>,
    #[account(mut)]
    pub payer: Signer<'info>,
    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,
}

#[account(zero_copy)]
#[derive(BorshSerialize, BorshDeserialize)]
pub struct FeeManager {
    timestamp: i64,
    authority: Option<Pubkey>
}

#[account(zero_copy)]
pub struct State {
    pub fee: NUMBER,
    pub x: NUMBER,
    pub y: NUMBER,
    pub enabled: FLAG,
    pub owner: Option<Pubkey>,
    pub fee_manager: Option<FeeManager>
}
