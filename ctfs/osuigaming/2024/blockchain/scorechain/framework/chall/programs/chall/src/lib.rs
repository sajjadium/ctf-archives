use anchor_lang::prelude::*;

pub use anchor_lang;

//pub const MAXIMUM_TRIES: u8 = 3;

// size of every account
// good enough for everything tbh lol
pub const ACCOUNT_SIZE: usize = 512;

declare_id!("Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS");

#[program]
pub mod chall {
    use anchor_lang::system_program;

    use super::*;

    pub fn init_db(_ctx: Context<InitDb>) -> Result<()> {
        Ok(())
    }

    pub fn submit_play(ctx: Context<SubmitPlay>, play: Play) -> Result<()> {
        let db = &mut ctx.accounts.db;
        let player = &mut ctx.accounts.player;

        let mut new_top = false;

        // check if there is an old play on the same map
        // if this play is better, award bounty and remove old play
        if let Some(idx) =  db.plays.iter().position(|x| &x.map == &play.map) {
            let old_play = &db.plays[idx];

            if play.pp > old_play.pp {
                **db.to_account_info().lamports.borrow_mut() -= old_play.bounty;
                **player.to_account_info().lamports.borrow_mut() += old_play.bounty;
                db.plays.remove(idx);
                new_top = true;
            }
        } else {
            new_top = true;
        }

        // new top play needs to deposit their bounty
        if new_top {
            let cpi_context = CpiContext::new(
                ctx.accounts.system_program.to_account_info(),
                system_program::Transfer {
                    from: player.to_account_info(),
                    to: db.to_account_info(),
                }
            );
            system_program::transfer(cpi_context, play.bounty)?;

            db.plays.push(play);
        }

        Ok(())
    }
}

#[derive(Accounts)]
pub struct InitDb<'info> {
    #[account(
        init,
        seeds = [ b"wysi" ],
        bump,
        payer = user,
        space = ACCOUNT_SIZE,
    )]
    pub db: Account<'info, PlayDb>,

    #[account(mut)]
    pub user: Signer<'info>,

    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,
}

#[derive(Accounts)]
pub struct SubmitPlay<'info> {
    #[account(
        mut,
        seeds = [ b"wysi" ],
        bump,
    )]
    pub db: Account<'info, PlayDb>,

    #[account(mut)]
    pub player: Signer<'info>,

    pub system_program: Program<'info, System>,
}

#[derive(Debug)]
#[account]
pub struct PlayDb {
    pub plays: Vec<Play>,
}
#[derive(Debug, AnchorSerialize, AnchorDeserialize, Clone)]
pub struct Play {
    pub map: String,
    pub player: String,
    pub pp: u64,
    pub bounty: u64,
}