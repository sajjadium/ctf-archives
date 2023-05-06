use anchor_lang::prelude::*;

use anchor_spl::token::{Mint, Token, TokenAccount};

declare_id!("28prS7e14Fsm97GE5ws2YpjxseFNkiA33tB5D3hLZv3t");

#[program]
pub mod solve {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {

        let cpi_accounts = chall::cpi::accounts::Attempt {
            reserve: ctx.accounts.reserve.to_account_info(),
            record: ctx.accounts.user_record.to_account_info(),
            user_account: ctx.accounts.user_account.to_account_info(),
            mint: ctx.accounts.mint.to_account_info(),
            user: ctx.accounts.user.to_account_info(),
            token_program: ctx.accounts.token_program.to_account_info(),
        };
        let cpi_ctx = CpiContext::new(ctx.accounts.chall.to_account_info(), cpi_accounts);
        chall::cpi::attempt(cpi_ctx)?;

        // --------------------------------------------
        // your instruction goes here


        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(mut)]
    pub admin: AccountInfo<'info>,

    #[account(mut)]
    pub config: AccountInfo<'info>,

    #[account(mut)]
    pub reserve: Account<'info, TokenAccount>,

    #[account(mut)]
    pub user_record: AccountInfo<'info>,

    #[account(mut)]
    pub user_account: Account<'info, TokenAccount>,

    #[account(mut)]
    pub user: Signer<'info>,

    pub mint: Account<'info, Mint>,

    pub token_program: Program<'info, Token>,

    pub system_program: Program<'info, System>,

    pub chall: Program<'info, chall::program::Chall>,

    pub rent: Sysvar<'info, Rent>,
}
