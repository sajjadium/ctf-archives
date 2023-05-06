use std::{ str::FromStr, convert::TryFrom, mem::size_of };
use anchor_lang::prelude::*;
use anchor_lang::solana_program::entrypoint::ProgramResult;
use anchor_spl::token::{self, Mint, TokenAccount, MintTo, Burn, Transfer, Token};

declare_id!("HPyMpt2qxYjifYVkeXEGqbqX4BB4zrLj1Bw69xTTPyFn");

const MASTER: &str = "6DKhzUFaCcgYeto3sea2xPDFqQBu1Ag8Z7t8Zz9t4eT1";

const STATE: &[u8]   = b"STATE";
const POOL: &[u8]    = b"POOL";
const TOKEN: &[u8]   = b"TOKEN";
const VOUCHER: &[u8] = b"VOUCHER";

#[program]
#[deny(unused_must_use)]
pub mod challenge2 {
    use super::*;

    pub fn setup_for_player(ctx: Context<SetupForPlayer>) -> ProgramResult {
        msg!("challenge2 setup_for_player");

        let state_seed: &[&[u8]] = &[ctx.accounts.player.key.as_ref(), STATE];
        let (_, state_bump) = Pubkey::find_program_address(state_seed, ctx.program_id);

        ctx.accounts.state.bump = state_bump;

        Ok(())
    }

    pub fn add_pool(ctx: Context<AddPool>, pool_index: u8) -> ProgramResult {
        msg!("challenge2 add_pool");

        let deposit_mint = ctx.accounts.deposit_mint.key();
        let pool_seed: &[&[u8]] = &[ctx.accounts.player.key.as_ref(), POOL, deposit_mint.as_ref()];
        let (_, pool_bump) = Pubkey::find_program_address(pool_seed, ctx.program_id);

        ctx.accounts.state.pools[pool_index as usize] = ctx.accounts.pool.key();

        ctx.accounts.pool.bump = pool_bump;
        ctx.accounts.pool.deposit_mint = ctx.accounts.deposit_mint.key();
        ctx.accounts.pool.pool_account = ctx.accounts.pool_account.key();
        ctx.accounts.pool.voucher_mint = ctx.accounts.voucher_mint.key();
        ctx.accounts.pool.decimals = ctx.accounts.deposit_mint.decimals;

        Ok(())
    }

    pub fn deposit(ctx: Context<DepositWithdraw>, amount: u64) -> ProgramResult {
        msg!("challenge2 deposit");

        if amount == 0 || amount > ctx.accounts.depositor_account.amount {
            return Err(ProgramError::InvalidArgument);
        }

        let state_seed: &[&[&[u8]]] = &[&[ctx.accounts.player.key.as_ref(), STATE, &[ctx.accounts.state.bump]]];

        let transfer_ctx = CpiContext::new(
            ctx.accounts.token_program.to_account_info(),
            Transfer {
                from: ctx.accounts.depositor_account.to_account_info(),
                to: ctx.accounts.pool_account.to_account_info(),
                authority: ctx.accounts.depositor.to_account_info(),
            },
        );

        token::transfer(transfer_ctx, amount)?;

        let mint_ctx = CpiContext::new_with_signer(
            ctx.accounts.token_program.to_account_info(),
            MintTo {
                mint: ctx.accounts.voucher_mint.to_account_info(),
                to: ctx.accounts.depositor_voucher_account.to_account_info(),
                authority: ctx.accounts.state.to_account_info(),
            },
            state_seed,
        );

        token::mint_to(mint_ctx, amount)?;

        Ok(())
    }

    pub fn withdraw(ctx: Context<DepositWithdraw>, amount: u64) -> ProgramResult {
        msg!("challenge2 withdraw");

        if amount == 0 || amount > ctx.accounts.depositor_voucher_account.amount {
            return Err(ProgramError::InvalidArgument);
        }

        let state_seed: &[&[&[u8]]] = &[&[ctx.accounts.player.key.as_ref(), STATE, &[ctx.accounts.state.bump]]];

        let burn_ctx = CpiContext::new(
            ctx.accounts.token_program.to_account_info(),
            Burn {
                mint: ctx.accounts.voucher_mint.to_account_info(),
                from: ctx.accounts.depositor_voucher_account.to_account_info(),
                authority: ctx.accounts.depositor.to_account_info(),
            },
        );

        token::burn(burn_ctx, amount)?;

        let transfer_ctx = CpiContext::new_with_signer(
            ctx.accounts.token_program.to_account_info(),
            Transfer {
                from: ctx.accounts.pool_account.to_account_info(),
                to: ctx.accounts.depositor_account.to_account_info(),
                authority: ctx.accounts.state.to_account_info(),
            },
            state_seed,
        );

        token::transfer(transfer_ctx, amount)?;

        Ok(())
    }

    pub fn swap(ctx: Context<Swap>, from_amount: u64) -> ProgramResult {
        msg!("challenge2 swap");

        if from_amount == 0 || from_amount > ctx.accounts.from_swapper_account.amount {
            return Err(ProgramError::InvalidArgument);
        }

        let to_amount = u64::try_from(
            u128::from(from_amount)
            .checked_mul(10_u128.pow(ctx.accounts.to_pool.decimals.into())) .unwrap()
            .checked_div(10_u128.pow(ctx.accounts.from_pool.decimals.into())).unwrap()
        ).unwrap();

        let check_amount = u64::try_from(
            u128::from(to_amount)
            .checked_mul(10_u128.pow(ctx.accounts.from_pool.decimals.into())).unwrap()
            .checked_div(10_u128.pow(ctx.accounts.to_pool.decimals.into())).unwrap()
        ).unwrap();

        if from_amount != check_amount {
            return Err(ProgramError::InvalidArgument);
        }

        let state_seed: &[&[&[u8]]] = &[&[ctx.accounts.player.key.as_ref(), STATE, &[ctx.accounts.state.bump]]];

        let transfer_in_ctx = CpiContext::new(
            ctx.accounts.token_program.to_account_info(),
            Transfer {
                from: ctx.accounts.from_swapper_account.to_account_info(),
                to: ctx.accounts.from_pool_account.to_account_info(),
                authority: ctx.accounts.swapper.to_account_info(),
            },
        );

        token::transfer(transfer_in_ctx, from_amount)?;

        let transfer_out_ctx = CpiContext::new_with_signer(
            ctx.accounts.token_program.to_account_info(),
            Transfer {
                from: ctx.accounts.to_pool_account.to_account_info(),
                to: ctx.accounts.to_swapper_account.to_account_info(),
                authority: ctx.accounts.state.to_account_info(),
            },
            state_seed,
        );

        token::transfer(transfer_out_ctx, to_amount)?;

        Ok(())
    }
}

#[derive(Accounts)]
pub struct SetupForPlayer<'info> {
    /// CHECK: shut up
    pub player: AccountInfo<'info>,
    #[account(mut/*, address = Pubkey::from_str(MASTER).unwrap()*/)]
    pub authority: Signer<'info>,
    #[account(
        init,
        seeds = [player.key().as_ref(), STATE],
        bump,
        payer = authority,
        space = 8 + size_of::<State>(),
    )]
    pub state: Account<'info, State>,
    pub rent: Sysvar<'info, Rent>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct AddPool<'info> {
    /// CHECK: shut up
    pub player: AccountInfo<'info>,
    #[account(mut/*, address = Pubkey::from_str(MASTER).unwrap()*/)]
    pub authority: Signer<'info>,
    #[account(
        mut,
        seeds = [player.key().as_ref(), STATE],
        bump = state.bump,
    )]
    pub state: Account<'info, State>,
    pub deposit_mint: Account<'info, Mint>,
    #[account(
        init,
        seeds = [player.key().as_ref(), POOL, deposit_mint.key().as_ref()],
        bump,
        payer = authority,
        space = 8 + size_of::<Pool>(),
    )]
    pub pool: Account<'info, Pool>,
    #[account(
        init,
        seeds = [player.key().as_ref(), TOKEN, deposit_mint.key().as_ref()],
        bump,
        token::mint = deposit_mint,
        token::authority = state,
        payer = authority,
    )]
    pub pool_account: Account<'info, TokenAccount>,
    #[account(
        init,
        seeds = [player.key().as_ref(), VOUCHER, deposit_mint.key().as_ref()],
        bump,
        mint::authority = state,
        mint::decimals = deposit_mint.decimals,
        payer = authority,
    )]
    pub voucher_mint: Account<'info, Mint>,
    pub rent: Sysvar<'info, Rent>,
    pub system_program: Program<'info, System>,
    pub token_program: Program<'info, Token>,
}

#[derive(Accounts)]
pub struct DepositWithdraw<'info> {
    /// CHECK: shut up
    pub player: AccountInfo<'info>,
    pub depositor: Signer<'info>,
    #[account(seeds = [player.key().as_ref(), STATE], bump = state.bump)]
    pub state: Account<'info, State>,
    pub deposit_mint: Account<'info, Mint>,
    #[account(constraint = state.pools.contains(&pool.key()))]
    pub pool: Account<'info, Pool>,
    #[account(mut, address = pool.pool_account)]
    pub pool_account: Box<Account<'info, TokenAccount>>,
    #[account(mut, seeds = [player.key().as_ref(), VOUCHER, deposit_mint.key().as_ref()], bump)]
    pub voucher_mint: Box<Account<'info, Mint>>,
    #[account(mut, constraint =  depositor_account.mint == pool.deposit_mint)]
    pub depositor_account: Box<Account<'info, TokenAccount>>,
    #[account(mut, constraint = depositor_voucher_account.mint == voucher_mint.key())]
    pub depositor_voucher_account: Box<Account<'info, TokenAccount>>,
    pub token_program: Program<'info, Token>,
}

#[derive(Accounts)]
pub struct Swap<'info> {
    /// CHECK: shut up
    pub player: AccountInfo<'info>,
    pub swapper: Signer<'info>,
    #[account(seeds = [player.key().as_ref(), STATE], bump = state.bump)]
    pub state: Account<'info, State>,
    #[account(constraint = state.pools.contains(&from_pool.key()))]
    pub from_pool: Account<'info, Pool>,
    #[account(constraint = state.pools.contains(&to_pool.key()) && from_pool.key() != to_pool.key())]
    pub to_pool: Account<'info, Pool>,
    #[account(mut, address = from_pool.pool_account)]
    pub from_pool_account: Box<Account<'info, TokenAccount>>,
    #[account(mut, address = to_pool.pool_account)]
    pub to_pool_account: Box<Account<'info, TokenAccount>>,
    #[account(mut, constraint = from_swapper_account.mint == from_pool.deposit_mint)]
    pub from_swapper_account: Box<Account<'info, TokenAccount>>,
    #[account(mut, constraint = to_swapper_account.mint == to_pool.deposit_mint)]
    pub to_swapper_account: Box<Account<'info, TokenAccount>>,
    pub token_program: Program<'info, Token>,
}
#[account]
#[derive(Default)]
pub struct State {
    bump: u8,
    pools: [Pubkey; 3],
}

#[account]
#[derive(Default)]
pub struct Pool {
    bump: u8,
    deposit_mint: Pubkey,
    pool_account: Pubkey,
    voucher_mint: Pubkey,
    decimals: u8,
}
