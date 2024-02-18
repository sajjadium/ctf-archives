use anchor_lang::prelude::*;
use anchor_lang::{InstructionData, ToAccountMetas};
use anchor_spl::token::{Mint, Token, TokenAccount};
use solana_program::{
    account_info::AccountInfo,
    instruction::Instruction,
    program::{invoke, invoke_signed},
    program_pack::Pack,
    pubkey::Pubkey,
    rent::Rent,
    system_instruction,
};

declare_id!("By8vGfgrrrWhcVy6F1mw6QGfhEvxLUHGs1DM1zt3YvLE");

#[program]
mod zerocoin {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>, bal: u64) -> Result<()> {
        invoke(
            &system_instruction::transfer(ctx.accounts.payer.key, ctx.accounts.vault.key, bal),
            &[
                ctx.accounts.payer.to_account_info(),
                ctx.accounts.vault.to_account_info(),
            ],
        )?;
        Ok(())
    }

    pub fn register(ctx: Context<Register>, user: Pubkey) -> Result<()> {
        assert_eq!(ctx.accounts.token.lamports(), 0);
        invoke(
            &Instruction::new_with_bytes(
                ID,
                &crate::instruction::CreateAccountHelper { user }.data(),
                crate::accounts::CreateAccountHelper {
                    token: ctx.accounts.token.key(),
                    vault: ctx.accounts.vault.key(),
                    system_program: ctx.accounts.system_program.key(),
                }
                .to_account_metas(None),
            ),
            &[
                ctx.accounts.token.to_account_info(),
                ctx.accounts.vault.to_account_info(),
                ctx.accounts.system_program.to_account_info(),
            ],
        )?;
        invoke(
            &spl_token::instruction::initialize_account3(
                &spl_token::ID,
                &ctx.accounts.token.key(),
                &ctx.accounts.mint.key(),
                &ctx.accounts.vault.key(),
            )?,
            &[
                ctx.accounts.token.to_account_info(),
                ctx.accounts.mint.to_account_info(),
            ],
        )?;
        Ok(())
    }

    pub fn create_account_helper(ctx: Context<CreateAccountHelper>, user: Pubkey) -> Result<()> {
        let _ = user;
        let space = spl_token::state::Account::LEN;
        invoke_signed(
            &system_instruction::create_account(
                &ctx.accounts.vault.key(),
                &ctx.accounts.token.key(),
                Rent::get()?.minimum_balance(space),
                space as u64,
                &spl_token::ID,
            ),
            &[
                ctx.accounts.token.to_account_info(),
                ctx.accounts.vault.to_account_info(),
                ctx.accounts.system_program.to_account_info(),
            ],
            &[
                &[b"vault", &[ctx.bumps.vault]],
                &[b"token", user.as_ref(), &[ctx.bumps.token]],
            ],
        )?;
        Ok(())
    }

    pub fn buy_zerocoin(ctx: Context<BuyZerocoin>, amt: u64) -> Result<()> {
        if amt == 0 {
            return Ok(());
        }
        let price = amt.checked_mul(7133742).unwrap();
        invoke(
            &system_instruction::transfer(
                &ctx.accounts.user.key(),
                &ctx.accounts.vault.key(),
                price,
            ),
            &[
                ctx.accounts.user.to_account_info(),
                ctx.accounts.vault.to_account_info(),
                ctx.accounts.system_program.to_account_info(),
            ],
        )?;
        invoke_signed(
            &spl_token::instruction::mint_to(
                &spl_token::ID,
                &ctx.accounts.mint.key(),
                &ctx.accounts.token.key(),
                &ctx.accounts.vault.key(),
                &[],
                amt,
            )?,
            &[
                ctx.accounts.mint.to_account_info(),
                ctx.accounts.token.to_account_info(),
                ctx.accounts.vault.to_account_info(),
            ],
            &[&[b"vault", &[ctx.bumps.vault]]],
        )?;
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(
        init,
        payer = payer,
        mint::decimals = 0,
        mint::authority = vault.key(),
        seeds = [b"mint"],
        bump
    )]
    mint: Account<'info, Mint>,
    #[account(mut)]
    payer: Signer<'info>,
    #[account(mut, seeds = [b"vault"], bump)]
    vault: SystemAccount<'info>,
    token_program: Program<'info, Token>,
    system_program: Program<'info, System>,
}

#[derive(Accounts)]
#[instruction(user: Pubkey)]
pub struct Register<'info> {
    #[account(
        mut,
        seeds = [b"token", user.as_ref()],
        bump
    )]
    token: AccountInfo<'info>,
    #[account(mut, seeds = [b"vault"], bump)]
    vault: SystemAccount<'info>,
    mint: AccountInfo<'info>,
    zerocoin: Program<'info, crate::program::Zerocoin>,
    token_program: Program<'info, Token>,
    system_program: Program<'info, System>,
}

#[derive(Accounts)]
#[instruction(user: Pubkey)]
pub struct CreateAccountHelper<'info> {
    #[account(
        mut,
        seeds = [b"token", user.as_ref()],
        bump
    )]
    token: AccountInfo<'info>,
    #[account(mut, seeds = [b"vault"], bump)]
    vault: SystemAccount<'info>,
    system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct BuyZerocoin<'info> {
    #[account(
        mut,
        seeds = [b"token", user.key().as_ref()],
        token::mint = mint.key(),
        token::authority = vault.key(),
        bump
    )]
    token: Account<'info, TokenAccount>,
    #[account(mut)]
    user: Signer<'info>,
    #[account(mut, seeds = [b"mint"], bump)]
    mint: Account<'info, Mint>,
    #[account(mut, seeds = [b"vault"], bump)]
    vault: SystemAccount<'info>,
    token_program: Program<'info, Token>,
    system_program: Program<'info, System>,
}
