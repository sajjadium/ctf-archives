use anchor_lang::prelude::*;

declare_id!("28prS7e14Fsm97GE5ws2YpjxseFNkiA33tB5D3hLZv3t");

#[program]
pub mod solve {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        // solve goes here:

        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    // feel free to expand/change this as needed
    // if you change this, make sure to change framework-solve/src/main.rs accordingly

    #[account(mut)]
    pub admin: AccountInfo<'info>,

    #[account(mut)]
    pub rich_boi: AccountInfo<'info>,

    #[account(mut)]
    pub user: Signer<'info>,

    #[account(mut)]
    pub auction: AccountInfo<'info>,

    #[account(mut)]
    pub product: AccountInfo<'info>,

    pub system_program: Program<'info, System>,

    pub chall: Program<'info, chall::program::Chall>,

    pub rent: Sysvar<'info, Rent>,
}