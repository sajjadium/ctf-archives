use anchor_lang::prelude::*;

pub use anchor_lang;

pub const MAXIMUM_TRIES: u8 = 3;

// size of every account
// good enough for everything tbh lol
pub const ACCOUNT_SIZE: usize = 256;


declare_id!("Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS");

#[program]
pub mod chall {
    use anchor_lang::system_program;

    use super::*;

    pub fn create_auction(ctx: Context<CreateAuction>, auction_name: Vec<u8>) -> Result<()> {

        let auction = &mut ctx.accounts.auction;
        let product = &mut ctx.accounts.product;
        let seller = &ctx.accounts.seller;

        auction.name = auction_name;
        auction.product = product.key();
        auction.owner = seller.key();

        auction.winning_bid_amount = 0;
        auction.has_ended = false;

        product.is_auctioning = true;

        Ok(())
    }

    pub fn create_product(ctx: Context<CreateProduct>, product_name: Vec<u8>, product_id: [u8; 32]) -> Result<()> {
        let product = &mut ctx.accounts.product;
        let user = &ctx.accounts.user;

        product.name = product_name;
        product.id = product_id;
        product.owner = user.key();
        product.is_auctioning = false;

        Ok(())
    }

    pub fn bid(ctx: Context<Bid>, bid_amount: u64) -> Result<()> {
        let auction = &mut ctx.accounts.auction;
        let bid = &mut ctx.accounts.bid;
        let bidder = &mut ctx.accounts.bidder;

        bid.auction = auction.key();
        bid.bidder = bidder.key();
        bid.amount = bid_amount;

        // we have already confirmed that bid amount is higher than what is currently winning using constraints
        // therefore we can just overwrite the current bid without any other checks
        auction.winning_bid = bid.key();
        auction.winning_bid_amount = bid_amount;
        auction.winning_bid_owner = bid.bidder;

        let cpi_context = CpiContext::new(
            ctx.accounts.system_program.to_account_info(),
            system_program::Transfer {
                from: bidder.to_account_info(),
                to: bid.to_account_info(),
            }
        );
        system_program::transfer(cpi_context, bid_amount)?;

        Ok(())
    }

    pub fn end_auction(ctx: Context<EndAuction>) -> Result<()> {
        let auction = &mut ctx.accounts.auction;
        let product = &mut ctx.accounts.product;

        auction.has_ended = true;

        product.owner = auction.winning_bid_owner;
        product.is_auctioning = false;

        Ok(())
    }

    pub fn recover_bid(ctx: Context<RecoverBid>) -> Result<()> {
        let bid = &mut ctx.accounts.bid;
        let user = &mut ctx.accounts.user;

        let cpi_context = CpiContext::new(
            ctx.accounts.system_program.to_account_info(),
            system_program::Transfer {
                from: bid.to_account_info(),
                to: user.to_account_info(),
            }
        );
        system_program::transfer(cpi_context, bid.amount)?;

        Ok(())
    }
}

#[derive(Accounts)]
#[instruction(auction_name: Vec<u8>)]
pub struct CreateAuction<'info> {
    #[account(
        init,
        seeds = [ product.key().as_ref(), &auction_name],
        bump,
        payer = seller,
        space = ACCOUNT_SIZE,
    )]
    pub auction: Account<'info, Auction>,

    #[account(
        mut,
        seeds = [ &product.name, &product.id ],
        bump,
        constraint = product.owner == seller.key(),
        constraint = !product.is_auctioning,
    )]
    pub product: Account<'info, Product>,

    #[account(mut)]
    pub seller: Signer<'info>,

    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,
}

#[derive(Accounts)]
#[instruction(product_name: Vec<u8>, product_id: [u8; 32])]
pub struct CreateProduct<'info> {
    #[account(
        init,
        seeds = [ &product_name[..], &product_id ],
        bump,
        payer = user,
        space = ACCOUNT_SIZE,
    )]
    pub product: Account<'info, Product>,

    #[account(mut)]
    pub user: Signer<'info>,

    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,
}

#[derive(Accounts)]
#[instruction(bid_amount: u64)]
pub struct Bid<'info> {
    #[account(
        init,
        seeds = [ &auction.key().as_ref(), &bidder.key().as_ref() ],
        bump,
        payer = bidder,
        space = ACCOUNT_SIZE,
    )]
    pub bid: Account<'info, BidInfo>,

    #[account(
        mut,
        seeds = [ product.key().as_ref(), &auction.name ],
        bump,
        constraint = !auction.has_ended,
        constraint = bid_amount > auction.winning_bid_amount,
    )]
    pub auction: Account<'info, Auction>,

    #[account(
        seeds = [ &product.name, &product.id ],
        bump,
    )]
    pub product: Account<'info, Product>,

    #[account(mut)]
    pub bidder: Signer<'info>,

    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,
}

#[derive(Accounts)]
pub struct EndAuction<'info> {
    #[account(
        mut,
        seeds = [ product.key().as_ref(), &auction.name],
        bump,
        constraint = !auction.has_ended,
        constraint = auction.owner == seller.key(),
        constraint = auction.winning_bid_amount > 0,
    )]
    pub auction: Account<'info, Auction>,

    #[account(
        mut,
        seeds = [ &product.name, &product.id ],
        bump,
    )]
    pub product: Account<'info, Product>,

    #[account(mut)]
    pub seller: Signer<'info>,

    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,
}

#[derive(Accounts)]
pub struct RecoverBid<'info> {
    #[account(
        mut,
        seeds = [ &auction.key().as_ref(), &user.key().as_ref() ],
        bump,
        constraint = (auction.winning_bid == bid.key() && user.key() == auction.owner) || (auction.winning_bid != bid.key() && user.key() == bid.bidder),
        constraint = bid.auction == auction.key(),
    )]
    pub bid: Account<'info, BidInfo>,

    #[account(
        mut,
        seeds = [ product.key().as_ref(), &auction.name ],
        bump,
        constraint = auction.has_ended || auction.winning_bid != bid.key(),
    )]
    pub auction: Account<'info, Auction>,

    #[account(
        seeds = [ &product.name, &product.id ],
        bump,
    )]
    pub product: Account<'info, Product>,

    #[account(mut)]
    pub user: Signer<'info>,

    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,
}

#[derive(Debug)]
#[account]
pub struct Auction {
    pub name: Vec<u8>,
    pub product: Pubkey,
    pub owner: Pubkey,

    pub winning_bid: Pubkey,
    pub winning_bid_amount: u64,
    pub winning_bid_owner: Pubkey,

    pub has_ended: bool,
}

#[derive(Debug)]
#[account]
pub struct Product {
    pub name: Vec<u8>,
    pub id: [u8; 32],

    pub owner: Pubkey,

    pub is_auctioning: bool,
}

#[derive(Debug)]
#[account]
pub struct BidInfo {
    pub auction: Pubkey,
    pub bidder: Pubkey,
    pub amount: u64,
}