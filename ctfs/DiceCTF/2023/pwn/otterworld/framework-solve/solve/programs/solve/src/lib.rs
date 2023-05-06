use anchor_lang::prelude::*;

use anchor_spl::token::Token;

declare_id!("osecio1111111111111111111111111111111111111");

#[program]
pub mod solve {
    use super::*;

    pub fn get_flag(_ctx: Context<GetFlag>) -> Result<()> {
        Ok(())
    }
}

#[derive(Accounts)]
pub struct GetFlag<'info> {
    #[account(mut)]
    pub state: AccountInfo<'info>,
    #[account(mut)]
    pub payer: Signer<'info>,

    pub system_program: Program<'info, System>,
    pub token_program: Program<'info, Token>,
    pub rent: Sysvar<'info, Rent>,
    pub chall: Program<'info, chall::program::Chall>
}
