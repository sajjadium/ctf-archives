use chall::anchor_lang::AccountDeserialize;
use chall::anchor_lang::InstructionData;
use chall::anchor_lang::ToAccountMetas;

use std::env;
use std::io::Write;

use sol_ctf_framework::ChallengeBuilder;

use solana_sdk::compute_budget::ComputeBudgetInstruction;

use solana_program::instruction::Instruction;
use solana_program::system_instruction;
use solana_program_test::tokio;
use solana_sdk::pubkey::Pubkey;
use solana_sdk::signature::Signer;
use solana_sdk::signer::keypair::Keypair;
use std::error::Error;

use std::net::{TcpListener, TcpStream};

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let listener = TcpListener::bind("0.0.0.0:1337")?;

    println!("starting server at port 1337!");

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        tokio::spawn(async {
            if let Err(err) = handle_connection(stream).await {
                println!("error: {:?}", err);
            }
        });
    }
    Ok(())
}

async fn handle_connection(mut socket: TcpStream) -> Result<(), Box<dyn Error>> {
    let mut builder = ChallengeBuilder::try_from(socket.try_clone().unwrap()).unwrap();

    let chall_id = builder.add_program("./chall/target/deploy/chall.so", Some(chall::ID));
    let solve_id = builder.input_program()?;

    let mut chall = builder.build().await;

    // -------------------------------------------------------------------------
    // [setup env] initialize
    // -------------------------------------------------------------------------
    let program_id = chall_id;

    // admin has infinite money wauw
    let admin_keypair = &chall.ctx.payer;
    let admin = admin_keypair.pubkey();

    const PRODUCT_NAME: &[u8] = b"sakura miku noodle stopper";
    const AUCTION_NAME: &[u8] = b"fun auction";

    let product_id = solana_program::hash::hash(&(727_i32).to_le_bytes()).to_bytes();

    let product = Pubkey::find_program_address(&[PRODUCT_NAME, &product_id], &program_id).0;
    let auction = Pubkey::find_program_address(&[product.as_ref(), AUCTION_NAME], &program_id).0;

    let user_keypair = Keypair::new();
    let user = user_keypair.pubkey();

    let rich_boi_keypair = Keypair::new();
    let rich_boi = rich_boi_keypair.pubkey();

    chall
        .run_ix(system_instruction::transfer(
            &admin,
            &rich_boi,
            500_000_000_000_000,
        ))
        .await?;

    // ur poor :^c
    chall
        .run_ix(system_instruction::transfer(&admin, &user, 1_000_000_000))
        .await?;

    println!("\nNon-PDA Accounts created...\n");

    // create product that will be auctioned
    let ix = chall::instruction::CreateProduct {
        product_name: PRODUCT_NAME.to_vec(),
        product_id,
    };

    let ix_accounts = chall::accounts::CreateProduct {
        product,
        user: admin,
        system_program: solana_program::system_program::ID,
        rent: solana_program::sysvar::rent::ID,
    };
    chall
        .run_ix(Instruction::new_with_bytes(
            program_id,
            &ix.data(),
            ix_accounts.to_account_metas(None),
        ))
        .await?;

    // create auction
    let ix = chall::instruction::CreateAuction {
        auction_name: AUCTION_NAME.to_vec(),
    };
    let ix_accounts = chall::accounts::CreateAuction {
        auction,
        product,
        seller: admin,
        system_program: solana_program::system_program::ID,
        rent: solana_program::sysvar::rent::ID,
    };
    chall
        .run_ix(Instruction::new_with_bytes(
            program_id,
            &ix.data(),
            ix_accounts.to_account_metas(None),
        ))
        .await?;

    // provided info
    writeln!(socket, "admin: {}", admin)?;
    writeln!(socket, "rich_boi: {}", rich_boi)?;
    writeln!(socket, "user: {}", user)?;
    writeln!(socket, "auction: {}", auction)?;
    writeln!(socket, "product: {}", product)?;

    // you're not quite as rich as rich_boi
    // but you're faster!
    let bump_budget = ComputeBudgetInstruction::set_compute_unit_limit(10_000_000);
    let solve_ix = chall.read_instruction(solve_id)?;
    chall
        .run_ixs_full(&[bump_budget, solve_ix], &[&user_keypair], &user)
        .await.ok();

    // time for rich_boi to ruin everything :'c
    // ...unless? 😳
    let rich_boi_bid =
        Pubkey::find_program_address(&[auction.as_ref(), rich_boi.as_ref()], &program_id).0;

    let ix = chall::instruction::Bid {
        bid_amount: 100_000_000_000_000,
    };
    let ix_accounts = chall::accounts::Bid {
        bid: rich_boi_bid,
        auction,
        product,
        bidder: rich_boi,
        system_program: solana_program::system_program::ID,
        rent: solana_program::sysvar::rent::ID,
    };
    chall
        .run_ixs_full(
            &[Instruction::new_with_bytes(
                program_id,
                &ix.data(),
                ix_accounts.to_account_metas(None),
            )],
            &[&rich_boi_keypair],
            &rich_boi,
        )
        .await.ok();

    // auction is over!
    let ix = chall::instruction::EndAuction {};
    let ix_accounts = chall::accounts::EndAuction {
        auction,
        product,
        seller: admin,
        system_program: solana_program::system_program::ID,
        rent: solana_program::sysvar::rent::ID,
    };
    chall
        .run_ix(Instruction::new_with_bytes(
            program_id,
            &ix.data(),
            ix_accounts.to_account_metas(None),
        ))
        .await?;

    // did you win the auction?
    let product_account = chall::Product::try_deserialize(
        &mut chall
            .ctx
            .banks_client
            .get_account(product)
            .await?
            .unwrap()
            .data
            .as_ref(),
    )?;

    if product_account.owner == user {
        writeln!(socket, "congrats!")?;
        if let Ok(flag) = env::var("FLAG") {
            writeln!(socket, "flag: {:?}", flag)?;
        } else {
            writeln!(socket, "flag not found, please contact admin")?;
        }
    } else if product_account.owner == rich_boi {
        writeln!(socket, "rich_boi won the auction :'(")?;
    } else {
        writeln!(socket, "nobody won the auction...?")?;
    }

    Ok(())
}
