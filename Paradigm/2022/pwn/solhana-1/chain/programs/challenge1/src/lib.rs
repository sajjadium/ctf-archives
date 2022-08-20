use std::{ str::FromStr, mem::size_of };
use anchor_lang::prelude::*;
use anchor_lang::solana_program::{ program_option::COption, entrypoint::ProgramResult };
use anchor_spl::token::{ self, Mint, TokenAccount, MintTo, Burn, Transfer, Token };

declare_id!("9NK3PnfnqMihgTbNuqjWCL6t8F4kPLqSz1wuj9wYxsoh");

const MASTER: &str = "6DKhzUFaCcgYeto3sea2xPDFqQBu1Ag8Z7t8Zz9t4eT1";

const STATE: &[u8]   = b"STATE";
const TOKEN: &[u8]   = b"TOKEN";
const VOUCHER: &[u8] = b"VOUCHER";

#[program]
#[deny(unused_must_use)]
pub mod challenge1 {
    use super::*;

    pub fn setup_for_player(ctx: Context<SetupForPlayer>) -> ProgramResult {
        msg!("challenge1 setup_for_player");

        let state_seed: &[&[u8]] = &[ctx.accounts.player.key.as_ref(), STATE];
        let (_, state_bump) = Pubkey::find_program_address(state_seed, ctx.program_id);

        ctx.accounts.state.bump = state_bump;
        ctx.accounts.state.deposit_account = ctx.accounts.deposit_account.key();
        ctx.accounts.state.deposit_mint = ctx.accounts.deposit_mint.key();

        Ok(())
    }

    pub fn deposit(ctx: Context<Transact>, amount: u64) -> ProgramResult {
        msg!("challenge1 deposit");

        let state_seed: &[&[&[u8]]] = &[&[ctx.accounts.player.key.as_ref(), STATE, &[ctx.accounts.state.bump]]];

        token::transfer(CpiContext::new(
            ctx.accounts.token_program.to_account_info(),
            Transfer {
                from: ctx.accounts.depositor_account.to_account_info(),
                to: ctx.accounts.deposit_account.to_account_info(),
                authority: ctx.accounts.depositor.to_account_info(),
            },
        ), amount)?;

        token::mint_to(CpiContext::new_with_signer(
            ctx.accounts.token_program.to_account_info(),
            MintTo {
                mint: ctx.accounts.voucher_mint.to_account_info(),
                to: ctx.accounts.depositor_voucher_account.to_account_info(),
                authority: ctx.accounts.state.to_account_info(),
            },
            state_seed,
        ), amount)?;

        Ok(())
    }

    pub fn withdraw(ctx: Context<Transact>, amount: u64) -> ProgramResult {
        msg!("challenge1 withdraw");

        let state_seed: &[&[&[u8]]] = &[&[ctx.accounts.player.key.as_ref(), STATE, &[ctx.accounts.state.bump]]];

        token::burn(CpiContext::new(
            ctx.accounts.token_program.to_account_info(),
            Burn {
                mint: ctx.accounts.voucher_mint.to_account_info(),
                from: ctx.accounts.depositor_voucher_account.to_account_info(),
                authority: ctx.accounts.depositor.to_account_info(),
            },
        ), amount)?;

        token::transfer(CpiContext::new_with_signer(
            ctx.accounts.token_program.to_account_info(),
            Transfer {
                from: ctx.accounts.deposit_account.to_account_info(),
                to: ctx.accounts.depositor_account.to_account_info(),
                authority: ctx.accounts.state.to_account_info(),
            },
            state_seed,
        ), amount)?;

        Ok(())
    }
}

#[derive(Accounts)]
pub struct SetupForPlayer<'info> {
    /// CHECK: shut up
    pub player: AccountInfo<'info>,
    #[account(mut/*, address = Pubkey::from_str(MASTER).unwrap()*/)]
    pub authority: Signer<'info>,
    #[account(
        init,
        seeds = [player.key().as_ref(), STATE],
        bump,
        payer = authority,
        space = 8 + size_of::<State>(),
    )]
    pub state: Account<'info, State>,
    #[account(
        init,
        seeds = [player.key().as_ref(), TOKEN],
        bump,
        token::mint = deposit_mint,
        token::authority = state,
        payer = authority,
    )]
    pub deposit_account: Account<'info, TokenAccount>,
    pub deposit_mint: Account<'info, Mint>,
    #[account(
        init,
        seeds = [player.key().as_ref(), VOUCHER],
        bump,
        mint::authority = state,
        mint::decimals = deposit_mint.decimals,
        payer = authority,
    )]
    pub voucher_mint: Account<'info, Mint>,
    pub rent: Sysvar<'info, Rent>,
    pub system_program: Program<'info, System>,
    pub token_program: Program<'info, Token>,
}

#[derive(Accounts)]
pub struct Transact<'info> {
    // player isnt a signer because, remember, player PUBKEY is a credential
    // pls dont make me implement a signing scheme for the flag fetching
    // im so tired of working on the server ill do it next time
    /// CHECK: shut up
    pub player: AccountInfo<'info>,
    pub depositor: Signer<'info>,
    #[account(seeds = [player.key().as_ref(), STATE], bump = state.bump)]
    pub state: Account<'info, State>,
    #[account(mut, address = state.deposit_account)]
    pub deposit_account: Account<'info, TokenAccount>,
    #[account(mut, constraint = voucher_mint.mint_authority == COption::Some(state.key()))]
    pub voucher_mint: Account<'info, Mint>,
    #[account(mut, constraint = depositor_account.mint == state.deposit_mint)]
    pub depositor_account: Account<'info, TokenAccount>,
    #[account(mut, constraint = depositor_voucher_account.mint == voucher_mint.key())]
    pub depositor_voucher_account: Account<'info, TokenAccount>,
    pub token_program: Program<'info, Token>,
}

#[account]
#[derive(Default)]
pub struct State {
    bump: u8,
    deposit_account: Pubkey,
    deposit_mint: Pubkey,
}
