use anchor_lang::prelude::*;
use anchor_spl::token::{Mint, Token, TokenAccount, Transfer};
use anchor_spl::token;

pub use anchor_lang;
pub use anchor_spl;


pub const MAXIMUM_CATALOG_SIZE: usize = 10;
pub const MAXIMUM_STRING_SIZE: usize = 30;


declare_id!("Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS");




#[program]
pub mod chall {
    use super::*;

    pub fn initialize(_ctx: Context<Initialize>) -> Result<()> {
        Ok(())
    }


    pub fn register(ctx: Context<Register>, org_name: String, employee_id: String) -> Result<()> {
        msg!("[CHALL] register: org {}, id {}", org_name, employee_id);
        require!(
            org_name.len() < MAXIMUM_STRING_SIZE,
            CoreError::StringTooLong
        );

        require!(
            employee_id.len() < MAXIMUM_STRING_SIZE,
            CoreError::StringTooLong
        );

        let catalog = &mut ctx.accounts.catalog;
        require!(
            ! ( catalog.orgs.contains(&org_name) && catalog.ids.contains(&employee_id) ),
            CoreError::DuplicatedEmployee
        );
        catalog.orgs.push(org_name.clone());
        catalog.ids.push(employee_id.clone());

        let employee_record = &mut ctx.accounts.employee_record;
        let employee_key = ctx.accounts.user.key();
        employee_record.org = org_name;
        employee_record.id  = employee_id;
        employee_record.key = employee_key;
        
        Ok(())
    }


    pub fn deposit(ctx: Context<Deposit>, org_name: String, employee_id: String, amount: u64) -> Result<()> {
        msg!("[CHALL] deposit");
        let vault = &mut ctx.accounts.vault;
        let employee_record = & ctx.accounts.employee_record;
        let user = & ctx.accounts.user;
        
        require!(
            user.key() == employee_record.key && org_name == employee_record.org && employee_id == employee_record.id,
            CoreError::UnknownEmployee
        );

        let deposit_ctx = CpiContext::new(
            ctx.accounts.token_program.to_account_info(),
            Transfer {
                from: ctx.accounts.user_token_account.to_account_info(),
                to: ctx.accounts.reserve.to_account_info(),
                authority: ctx.accounts.user.to_account_info()
            }
        );
        token::transfer(deposit_ctx, amount)?;

        vault.amount += amount;

        Ok(())
    }


    pub fn withdraw(ctx: Context<Withdraw>, org_name: String, employee_id: String, amount: u64) -> Result<()> {
        msg!("[CHALL] withdraw");
        let vault = &mut ctx.accounts.vault;
        let employee_record = & ctx.accounts.employee_record;
        let payer = ctx.accounts.payer.key();
        
        require!(
            payer == employee_record.key && org_name == employee_record.org && employee_id == employee_record.id,
            CoreError::UnknownEmployee
        );
        require!(
            vault.amount >= amount,
            CoreError::InsufficientBalance
        );

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

        vault.amount -= amount;

        Ok(())
    }

}

// --------------------------------------------------------------

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(
        init,
        seeds = [ b"CATALOG" ],
        bump,   
        payer = payer,
        space = Catalog::SIZE,
    )]
    pub catalog: Account<'info, Catalog>,

    #[account(
        init,
        seeds = [ b"RESERVE" ],
        bump,
        payer = payer,
        token::mint = mint,
        token::authority = reserve
    )]
    pub reserve: Account<'info, TokenAccount>,

    pub mint: Account<'info, Mint>,

    #[account(mut)]
    pub payer: Signer<'info>,
    pub token_program: Program<'info, Token>,
    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,
}

#[account]
#[repr(C, align(8))]
#[derive(Default)]
pub struct Catalog {
    pub orgs: Vec<String>,
    pub ids: Vec<String>,
}

impl Catalog {
    pub const SIZE : usize = 8 
        + 4 + (4 + MAXIMUM_STRING_SIZE) * MAXIMUM_CATALOG_SIZE   // orgs: Vec<String>,
        + 4 + (4 + MAXIMUM_STRING_SIZE) * MAXIMUM_CATALOG_SIZE;  //  ids: Vec<String>,
}

// --------------------------------------------------------------

#[derive(Accounts)]
pub struct Register<'info> {
    #[account(
        mut,
        seeds = [ b"CATALOG" ],
        bump
    )]
    pub catalog: Account<'info, Catalog>,

    #[account(
        init,
        seeds = [user.key().as_ref()],
        bump,
        payer = user,
        space = EmployeeRecord::SIZE,
    )]
    pub employee_record: Account<'info, EmployeeRecord>,

    #[account(mut)]
    pub user: Signer<'info>,
    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,
}

#[account]
#[repr(C, align(8))]
#[derive(Default)]
pub struct EmployeeRecord {
    pub org: String,
    pub id: String,
    pub key: Pubkey,
}

impl EmployeeRecord {
    pub const SIZE : usize = 8 
        + 4 + MAXIMUM_STRING_SIZE   // orgs: String,
        + 4 + MAXIMUM_STRING_SIZE   //  ids: String,
        + 32;                       //  key: Pubkey
}

// --------------------------------------------------------------

#[derive(Accounts)]
#[instruction(org_name: String, employee_id: String)]
pub struct Deposit<'info> {
    #[account(
        init_if_needed,
        seeds = [org_name.as_bytes(), employee_id.as_bytes()],
        bump,
        space = Vault::SIZE,
        payer = user 
    )]
    pub vault: Account<'info, Vault>,

    #[account(
        seeds = [user.key().as_ref()],
        bump,
        constraint = employee_record.org == org_name,
        constraint = employee_record.id == employee_id,
        constraint = employee_record.key == user.key(),
    )]
    pub employee_record: Account<'info, EmployeeRecord>,

    #[account(
        mut,
        seeds = [ b"RESERVE" ],
        bump,
        constraint = reserve.mint == mint.key(),
    )]
    pub reserve: Account<'info, TokenAccount>,

    #[account(
        mut,
        constraint = user_token_account.owner == user.key(),
        constraint = user_token_account.mint  == mint.key()
    )]
    pub user_token_account: Account<'info, TokenAccount>,

    pub mint: Account<'info, Mint>,

    #[account(mut)]
    pub user: Signer<'info>,
    pub token_program: Program<'info, Token>,
    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,
}

#[account]
#[repr(C, align(8))]
#[derive(Default)]
pub struct Vault {
    pub amount : u64,
}

impl Vault {
    pub const SIZE : usize = 8 // DISCRIMINATOR_SIZE
        + 8;                   // u64
}

// --------------------------------------------------------------

#[derive(Accounts)]
#[instruction(org_name: String, employee_id: String)]
pub struct Withdraw<'info> {
    #[account(
        mut,
        seeds = [org_name.as_bytes(), employee_id.as_bytes()],
        bump,
    )]
    pub vault: Account<'info, Vault>,

    #[account(
        seeds = [payer.key().as_ref()],
        bump,
        constraint = employee_record.org == org_name,
        constraint = employee_record.id == employee_id,
        constraint = employee_record.key == payer.key(),
    )]
    pub employee_record: Account<'info, EmployeeRecord>,

    #[account(
        mut,
        seeds = [ b"RESERVE" ],
        bump,
        constraint = reserve.mint == mint.key(),
    )]
    pub reserve: Account<'info, TokenAccount>,

    #[account(
        mut,
        constraint = user_account.owner == payer.key(),
        constraint = user_account.mint  == mint.key()
    )]
    pub user_account: Account<'info, TokenAccount>,

    pub mint: Account<'info, Mint>,

    #[account(mut)]
    pub payer: Signer<'info>,
    pub token_program: Program<'info, Token>,
    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,
}


#[error_code]
pub enum CoreError {
    #[msg("The string is too long")]
    StringTooLong,
    #[msg("Duplicated employee")]
    DuplicatedEmployee,
    #[msg("Unknown employee")]
    UnknownEmployee,
    #[msg("Insufficient balance")]
    InsufficientBalance,
    #[msg("Bump not found")]
    BumpNotFound,
}
