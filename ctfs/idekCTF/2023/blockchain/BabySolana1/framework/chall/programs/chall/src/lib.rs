use anchor_lang::prelude::*;
use anchor_spl::token::{Mint, Token, TokenAccount, Transfer};
use anchor_spl::token;

pub use anchor_lang;
pub use anchor_spl;

pub const MAXIMUM_TRIES: u8 = 3;


declare_id!("Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS");




#[program]
pub mod chall {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        let config = &mut ctx.accounts.config;
        config.admin = ctx.accounts.admin.key();
        Ok(())
    }


    pub fn register(ctx: Context<Register>) -> Result<()> {
        let record = &mut ctx.accounts.user_record;
        record.user = ctx.accounts.user.key();
        record.tries = MAXIMUM_TRIES;
        msg!("[CHALL] register: user {}, tries {}", record.user, record.tries);
        Ok(())
    }


    pub fn attempt(ctx: Context<Attempt>) -> Result<()> {
        let record = &mut ctx.accounts.record;
        msg!("[CHALL] attempt.tries {}", record.tries);
        if record.tries > 0 {
            let reserve_bump = [*ctx.bumps.get("reserve").unwrap()];
            let signer_seeds = [
                b"RESERVE",
                reserve_bump.as_ref()
            ];
            let signer = &[&signer_seeds[..]];

            let withdraw_ctx = CpiContext::new_with_signer(
                ctx.accounts.token_program.to_account_info(),
                Transfer {
                    from: ctx.accounts.reserve.to_account_info(),
                    to: ctx.accounts.user_account.to_account_info(),
                    authority: ctx.accounts.reserve.to_account_info()
                },
                signer
            );
            token::transfer(withdraw_ctx, record.tries as u64)?;
        }
        record.tries -= 1;
        Ok(())
    }


    pub fn deposit(ctx: Context<Deposit>, amount: u64) -> Result<()> {
        let reserve_bump = [*ctx.bumps.get("reserve").unwrap()];
        let signer_seeds = [
            b"RESERVE",
            reserve_bump.as_ref()
        ];
        let signer = &[&signer_seeds[..]];

        let withdraw_ctx = CpiContext::new_with_signer(
            ctx.accounts.token_program.to_account_info(),
            Transfer {
                from: ctx.accounts.reserve.to_account_info(),
                to: ctx.accounts.user_account.to_account_info(),
                authority: ctx.accounts.reserve.to_account_info()
            },
            signer
        );
        token::transfer(withdraw_ctx, amount)?;
        Ok(())
    }

}

// --------------------------------------------------------------

#[account]
#[repr(C, align(8))]
#[derive(Default)]
pub struct Config {
    pub admin: Pubkey,
}

impl Config {
    pub const SIZE : usize = 8 
        + 32
        + 1;
}


#[account]
#[repr(C, align(8))]
#[derive(Default)]
pub struct UserRecord {
    pub user: Pubkey,
    pub tries: u8
}

impl UserRecord {
    pub const SIZE : usize = 8 
        + 32
        + 1;
}

// --------------------------------------------------------------

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(
        init,
        seeds = [ b"CONFIG" ],
        bump,   
        payer = admin,
        space = Config::SIZE,
    )]
    pub config: Account<'info, Config>,

    #[account(
        init,
        seeds = [ b"RESERVE" ],
        bump,
        payer = admin,
        token::mint = mint,
        token::authority = reserve
    )]
    pub reserve: Account<'info, TokenAccount>,

    pub mint: Account<'info, Mint>,
    #[account(mut)]
    pub admin: Signer<'info>,
    pub token_program: Program<'info, Token>,
    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,
}



#[derive(Accounts)]
pub struct Register<'info> {
    #[account(
        init,
        seeds = [user.key().as_ref()],
        bump,
        payer = user,
        space = UserRecord::SIZE,
    )]
    pub user_record: Account<'info, UserRecord>,

    #[account(
        init,
        seeds = [b"account", user.key().as_ref()],
        bump,
        payer = user,
        token::mint = mint,
        token::authority = user,
    )]
    pub user_account: Account<'info, TokenAccount>,

    pub mint: Account<'info, Mint>,

    #[account(mut)]
    pub user: Signer<'info>,
    pub token_program: Program<'info, Token>,
    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,
}



#[derive(Accounts)]
pub struct Attempt<'info> {
    #[account(
        mut,
        seeds = [ b"RESERVE" ],
        bump,
        constraint = reserve.mint == mint.key(),
    )]
    pub reserve: Account<'info, TokenAccount>,

    #[account(
        mut,
        seeds = [user.key().as_ref()],
        bump,
        has_one = user
    )]
    pub record: Account<'info, UserRecord>,

    #[account(
        mut,
        seeds = [b"account", user.key().as_ref()],
        bump,
        constraint = user_account.mint == mint.key(),
        constraint = user_account.owner == user.key(),
    )]
    pub user_account: Account<'info, TokenAccount>,

    pub mint: Account<'info, Mint>,

    #[account(mut)]
    pub user: Signer<'info>,
    pub token_program: Program<'info, Token>,
}


#[derive(Accounts)]
pub struct Deposit<'info> {
    #[account(
        mut,
        seeds = [ b"CONFIG" ],
        bump,
        has_one = admin
    )]
    pub config: Account<'info, Config>,

    #[account(
        mut,
        seeds = [ b"RESERVE" ],
        bump,
        constraint = reserve.mint == mint.key(),
    )]
    pub reserve: Account<'info, TokenAccount>,

    #[account(
        mut,
        seeds = [b"account", user.key().as_ref()],
        bump,
        constraint = user_account.mint == mint.key(),
        constraint = user_account.owner == user.key(),
    )]
    pub user_account: Account<'info, TokenAccount>,

    pub mint: Account<'info, Mint>,

    #[account(mut)]
    pub admin: AccountInfo<'info>,
    
    #[account(mut)]
    pub user:  Signer<'info>,
    pub token_program: Program<'info, Token>,
    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,
}



#[error_code]
pub enum CoreError {
    #[msg("The max_tries is too large")]
    MaxTriesTooLarge,
    #[msg("Bump not found")]
    BumpNotFound,
}
