use anchor_lang::prelude::*;

declare_id!("28prS7e14Fsm97GE5ws2YpjxseFNkiA33tB5D3hLZv3t");

#[program]
pub mod solve {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {

        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    // feel free to expand/change this as needed
    // if you change this, make sure to change framework-solve/src/main.rs accordingly

    #[account(mut)]
    pub mapper: Signer<'info>,

    #[account(mut)]
    pub admin: AccountInfo<'info>,

    #[account(mut)]
    pub bn: AccountInfo<'info>,

    #[account(mut)]
    pub config: AccountInfo<'info>,

    #[account(mut)]
    pub map: AccountInfo<'info>,

    pub chall: Program<'info, chall::program::Chall>,

    pub system_program: Program<'info, System>,
}
