use anchor_lang::prelude::*;

use anchor_spl::token::{Token, TokenAccount};

declare_id!("osecio1111111111111111111111111111111111111");

#[program]
pub mod solve {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        let cpi_accounts = chall::cpi::accounts::Swap {
            swap: ctx.accounts.swap.clone(),
            payer: ctx.accounts.payer.to_account_info(),
            pool_a: ctx.accounts.pool_a.to_account_info(),
            pool_b: ctx.accounts.pool_b.to_account_info(),

            user_in_account: ctx.accounts.user_in_account.to_account_info(),
            user_out_account: ctx.accounts.user_out_account.to_account_info(),

            token_program: ctx.accounts.token_program.to_account_info(),
        };

        let cpi_ctx = CpiContext::new(ctx.accounts.chall.to_account_info(), cpi_accounts);

        chall::cpi::swap(cpi_ctx, 10, true)?;

        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    pub swap: AccountInfo<'info>,
    #[account(mut)]
    pub pool_a: Account<'info, TokenAccount>,
    #[account(mut)]
    pub pool_b: Account<'info, TokenAccount>,

    #[account(mut)]
    pub user_in_account: Account<'info, TokenAccount>,
    #[account(mut)]
    pub user_out_account: Account<'info, TokenAccount>,

    #[account(mut)]
    pub payer: Signer<'info>,
    pub token_program: Program<'info, Token>,

    pub chall: Program<'info, chall::program::Chall>
}
