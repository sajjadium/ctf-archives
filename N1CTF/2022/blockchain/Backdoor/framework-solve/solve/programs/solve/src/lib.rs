use anchor_lang::prelude::*;

declare_id!("N1CTF11111111111111111111111111111111111111");

#[program]
pub mod solve {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        
        // TODO

        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    // TODO
}
