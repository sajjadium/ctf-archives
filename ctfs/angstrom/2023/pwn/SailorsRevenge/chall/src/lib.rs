mod entrypoint;
pub mod processor;

/*
fn transfer<'a>(
    from: &AccountInfo<'a>,
    to: &AccountInfo<'a>,
    amt: u64,
    signers: &[&[&[u8]]],
) -> Result<()> {
    if from.lamports() >= amt {
        invoke_signed(
            &system_instruction::transfer(from.key, to.key, amt),
            &[from.clone(), to.clone()],
            signers,
        )?;
    }
    Ok(())
}

#[program]
mod sailor {
    use super::*;

    pub fn create_union(ctx: Context<CreateUnion>, bal: u64) -> Result<()> {
        msg!("creating union {}", bal);

        if ctx.accounts.authority.lamports() >= bal {
            transfer(&ctx.accounts.authority, &ctx.accounts.vault, bal, &[])?;
            // initial balance isn't available because I said so
            ctx.accounts.sailor_union.available_funds = 0;
            ctx.accounts.sailor_union.authority = ctx.accounts.authority.key();
            Ok(())
        } else {
            msg!(
                "insufficient funds, have {} but need {}",
                ctx.accounts.authority.lamports(),
                bal
            );
            Err(ProgramError::InsufficientFunds.into())
        }
    }

    pub fn pay_dues(ctx: Context<PayDues>, amt: u64) -> Result<()> {
        msg!("paying dues {}", amt);

        if ctx.accounts.member.lamports() >= amt {
            ctx.accounts.sailor_union.available_funds += amt;
            transfer(&ctx.accounts.authority, &ctx.accounts.vault, amt, &[])?;
            Ok(())
        } else {
            msg!(
                "insufficient funds, have {} but need {}",
                ctx.accounts.member.lamports(),
                amt
            );
            Err(ProgramError::InsufficientFunds.into())
        }
    }

    pub fn strike_pay(ctx: Context<StrikePay>, amt: u64) -> Result<()> {
        msg!("strike pay {}", amt);

        let (_, vault_bump) = Pubkey::find_program_address(&[b"vault"], &ID);

        if ctx.accounts.sailor_union.available_funds >= amt {
            ctx.accounts.sailor_union.available_funds -= amt;
            transfer(
                &ctx.accounts.vault,
                &ctx.accounts.member,
                amt,
                &[&[b"vault", &[vault_bump]]],
            )?;
            Ok(())
        } else {
            msg!(
                "insufficient funds, have {} but need {}",
                ctx.accounts.sailor_union.available_funds,
                amt
            );
            Err(ProgramError::InsufficientFunds.into())
        }
    }
}

#[derive(Accounts)]
pub struct CreateUnion<'info> {
    #[account(
        init,
        payer = authority,
        space = 8 + std::mem::size_of::<SailorUnion>(),
        seeds = [b"union", authority.key.as_ref()],
        bump
    )]
    sailor_union: Account<'info, SailorUnion>,
    #[account(mut)]
    authority: Signer<'info>,
    #[account(mut, seeds = [b"vault"], bump)]
    vault: SystemAccount<'info>,
    system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct PayDues<'info> {
    #[account(mut)]
    sailor_union: Account<'info, SailorUnion>,
    member: SystemAccount<'info>,
    #[account(mut)]
    authority: Signer<'info>,
    #[account(mut, seeds = [b"vault"], bump)]
    vault: SystemAccount<'info>,
    system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct StrikePay<'info> {
    #[account(mut)]
    sailor_union: Account<'info, SailorUnion>,
    #[account(mut)]
    member: SystemAccount<'info>,
    authority: Signer<'info>,
    #[account(mut, seeds = [b"vault"], bump)]
    vault: SystemAccount<'info>,
    system_program: Program<'info, System>,
}

#[account]
pub struct SailorUnion {
    available_funds: u64,
    authority: Pubkey,
}
*/