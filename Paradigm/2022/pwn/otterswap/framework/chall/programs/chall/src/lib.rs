use anchor_lang::prelude::*;
use anchor_spl::token::{Mint, Token, TokenAccount, Transfer};
use anchor_spl::token;

pub use anchor_lang;
pub use anchor_spl;

pub const SWAP_SEED: &[u8] = b"swap";
pub const POOL_A_SEED: &[u8] = b"poolA";
pub const POOL_B_SEED: &[u8] = b"poolB";

declare_id!("Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS");

#[program]
pub mod chall {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        let swap = &mut ctx.accounts.swap;

        swap.owner = ctx.accounts.payer.key();
        swap.pool_a = ctx.accounts.pool_a.key();
        swap.pool_b = ctx.accounts.pool_b.key();
        swap.bump = [*ctx.bumps.get("swap").unwrap()];

        Ok(())
    }

    pub fn swap(ctx: Context<Swap>, amount: u64, a_to_b: bool) -> Result<()> {
        let swap = &ctx.accounts.swap;
        let pool_a = &mut ctx.accounts.pool_a;
        let pool_b = &mut ctx.accounts.pool_b;
        let user_in_account = &ctx.accounts.user_in_account;
        let user_out_account = &ctx.accounts.user_out_account;

        let (in_pool_account, out_pool_account) = if a_to_b { (pool_a, pool_b) } else { (pool_b, pool_a) };

        let x = in_pool_account.amount;
        let y = out_pool_account.amount;

        let out_amount = y - (x * y) / (x + amount);

        assert!(in_pool_account.mint == user_in_account.mint);
        assert!(out_pool_account.mint == user_out_account.mint);

        let in_ctx = CpiContext::new(
            ctx.accounts.token_program.to_account_info(),
            Transfer {
                from: ctx.accounts.user_in_account.to_account_info(),
                to: in_pool_account.to_account_info(),
                authority: ctx.accounts.payer.to_account_info()
            }
        );
        let out_ctx = CpiContext::new(
            ctx.accounts.token_program.to_account_info(),
            Transfer {
                from: out_pool_account.to_account_info(),
                to: ctx.accounts.user_out_account.to_account_info(),
                authority: ctx.accounts.swap.to_account_info()
            }
        );

        token::transfer(in_ctx, amount)?;
        let signer = [&swap.signer_seeds()[..]];
        token::transfer(out_ctx.with_signer(&signer), out_amount)?;

        in_pool_account.reload()?;
        out_pool_account.reload()?;

        assert!(in_pool_account.amount == x + amount);
        assert!(out_pool_account.amount == y - out_amount);

        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(
        init,
        seeds = [ SWAP_SEED, payer.key().as_ref() ],
        bump,
        payer = payer,
        space = 1000
    )]
    pub swap: Account<'info, SwapInfo>,

    #[account(init,
        seeds = [ POOL_A_SEED, swap.key().as_ref() ],
        bump,
        payer = payer,
        token::mint = mint_a,
        token::authority = swap
    )]
    pub pool_a: Account<'info, TokenAccount>,

    #[account(init,
        seeds = [ POOL_B_SEED, swap.key().as_ref() ],
        bump,
        payer = payer,
        token::mint = mint_b,
        token::authority = swap
    )]
    pub pool_b: Account<'info, TokenAccount>,

    #[account(constraint = mint_a.key() != mint_b.key())]
    pub mint_a: Account<'info, Mint>,
    #[account(constraint = mint_b.key() != mint_a.key())]
    pub mint_b: Account<'info, Mint>,

    #[account(mut)]
    pub payer: Signer<'info>,
    pub system_program: Program<'info, System>,
    pub token_program: Program<'info, Token>,
    pub rent: Sysvar<'info, Rent>,
}

#[derive(Accounts)]
pub struct Swap<'info> {
    #[account(
        has_one = pool_a,
        has_one = pool_b,
        seeds = [ SWAP_SEED, swap.owner.as_ref() ],
        bump = swap.bump[0]
    )]
    pub swap: Account<'info, SwapInfo>,

    #[account(mut,
        seeds = [ POOL_A_SEED, swap.key().as_ref() ],
        bump,
        token::authority = swap
    )]
    pub pool_a: Account<'info, TokenAccount>,

    #[account(mut,
        seeds = [ POOL_B_SEED, swap.key().as_ref() ],
        bump,
        token::authority = swap
    )]
    pub pool_b: Account<'info, TokenAccount>,

    #[account(mut,
        constraint = user_in_account.owner == payer.key()
    )]
    pub user_in_account: Account<'info, TokenAccount>,

    #[account(mut,
        constraint = user_out_account.owner == payer.key()
    )]
    pub user_out_account: Account<'info, TokenAccount>,

    #[account(mut)]
    pub payer: Signer<'info>,
    pub token_program: Program<'info, Token>,
}

#[account]
#[repr(C, align(8))]
#[derive(Default)]
pub struct SwapInfo {
    pub pool_a: Pubkey,
    pub pool_b: Pubkey,
    pub owner: Pubkey,
    pub bump: [u8; 1]
}

impl SwapInfo {
    pub fn signer_seeds(&self) -> [&[u8]; 3] {
        [
            SWAP_SEED,
            self.owner.as_ref(),
            self.bump.as_ref()
        ]
    }
}
