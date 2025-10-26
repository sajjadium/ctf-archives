use anchor_lang::prelude::*;

pub use anchor_lang;

// size of every account
// good enough for everything tbh lol
pub const ACCOUNT_SIZE: usize = 512;

declare_id!("Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS");

#[program]
pub mod chall {
    use super::*;

    pub fn init(ctx: Context<Init>) -> Result<()> {
        let config = &mut ctx.accounts.config;
        let admin = &ctx.accounts.admin;

        config.owner = admin.key();
        config.bn_list = Vec::new();

        Ok(())
    }

    pub fn add_bn(ctx: Context<AddBn>) -> Result<()> {
        let config = &mut ctx.accounts.config;
        let bn = &ctx.accounts.bn;

        if !config.bn_list.contains(bn.key) {
            config.bn_list.push(bn.key());
        }

        Ok(())
    }

    pub fn remove_bn(ctx: Context<RemoveBn>) -> Result<()> {
        let config = &mut ctx.accounts.config;
        let bn = &ctx.accounts.bn;

        let idx = config.bn_list.iter().position(|k| k == bn.key).expect("bn is not in list");
        config.bn_list.remove(idx);

        Ok(())
    }

    pub fn create_map(ctx: Context<CreateMap>, map_name: String) -> Result<()> {
        let map = &mut ctx.accounts.map;
        let mapper = &ctx.accounts.mapper;

        map.name = map_name;
        map.mapper = mapper.key();
        map.ranked = false;

        Ok(())
    }

    pub fn rank_map(ctx: Context<RankMap>) -> Result<()> {
        let map = &mut ctx.accounts.map;

        map.ranked = true;
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Init<'info> {
    #[account(
        init_if_needed,
        seeds = [ b"wysi" ],
        bump,
        payer = admin,
        space = ACCOUNT_SIZE,
    )]
    pub config: Account<'info, Config>,

    #[account(mut)]
    pub admin: Signer<'info>,

    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct AddBn<'info> {
    #[account(
        mut,
        seeds = [ b"wysi" ],
        bump,
    )]
    pub config: Account<'info, Config>,

    #[account(
        constraint = config.owner == admin.key()
    )]
    pub admin: Signer<'info>,

    pub bn: UncheckedAccount<'info>,
}

#[derive(Accounts)]
pub struct RemoveBn<'info> {
    #[account(
        mut,
        seeds = [ b"wysi" ],
        bump,
    )]
    pub config: Account<'info, Config>,

    #[account(
        constraint = config.owner == admin.key()
    )]
    pub admin: Signer<'info>,

    pub bn: UncheckedAccount<'info>,
}

#[derive(Accounts)]
#[instruction(map_name: String)]
pub struct CreateMap<'info> {
    #[account(
        init,
        seeds = [ b"map", map_name.as_bytes() ],
        bump,
        payer = mapper,
        space = ACCOUNT_SIZE,
    )]
    pub map: Account<'info, Map>,

    #[account(mut)]
    pub mapper: Signer<'info>,

    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct RankMap<'info> {
    #[account(
        seeds = [ b"wysi" ],
        bump,
    )]
    pub config: Account<'info, Config>,

    #[account(
        mut,
        seeds = [ b"map", map.name.as_bytes() ],
        bump,
        constraint = !map.ranked
    )]
    pub map: Account<'info, Map>,

    #[account(
        constraint = config.bn_list.contains(&bn.key())
    )]
    pub bn: Signer<'info>,
}

#[derive(Debug)]
#[account]
pub struct Config {
    pub owner: Pubkey,
    pub bn_list: Vec<Pubkey>,
}

#[derive(Debug)]
#[account]
pub struct Map {
    pub name: String,
    pub mapper: Pubkey,
    pub ranked: bool,
}
