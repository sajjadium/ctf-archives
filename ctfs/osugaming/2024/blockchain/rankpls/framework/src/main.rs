use chall::anchor_lang::AccountDeserialize;
use chall::anchor_lang::InstructionData;
use chall::anchor_lang::ToAccountMetas;
use solana_sdk::account::ReadableAccount;

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

    // peppy has infinite money wauw
    let peppy_keypair = chall.ctx.payer.insecure_clone();
    let peppy = peppy_keypair.pubkey();

    let (config, _) = Pubkey::find_program_address(&[ b"wysi" ], &program_id);
    let (map, _) = Pubkey::find_program_address(&[ b"map", b"harumachi zenith" ], &program_id);

    let mapper_keypair = Keypair::new();
    let mapper = mapper_keypair.pubkey();

    let bn_keypair = Keypair::new();
    let bn = bn_keypair.pubkey();

    //chall
    //    .run_ix(system_instruction::transfer(
    //        &admin,
    //        &cookiezi,
    //        500_000_000_000_000,
    //    ))
    //    .await?;

    chall
        .run_ix(system_instruction::transfer(&peppy, &mapper, 100_000_000))
        .await?;

    println!("\nNon-PDA Accounts created...\n");

    let init_ix = chall::instruction::Init {};
    let init_ix_accounts = chall::accounts::Init {
        config,
        admin: peppy,
        system_program: solana_program::system_program::ID,
    };
    let bn_ix = chall::instruction::AddBn {};
    let bn_ix_accounts = chall::accounts::AddBn {
        config,
        admin: peppy,
        bn,
    };
    chall
        .run_ixs_full(
            &[Instruction::new_with_bytes(
                program_id,
                &init_ix.data(),
                init_ix_accounts.to_account_metas(None)
                ),
                Instruction::new_with_bytes(
                    program_id,
                    &bn_ix.data(),
                    bn_ix_accounts.to_account_metas(None)
                ),
            ],
            &[&peppy_keypair],
            &peppy,
        ).await?;

    let map_ix = chall::instruction::CreateMap {
        map_name: String::from("harumachi zenith"),
    };
    let map_ix_accounts = chall::accounts::CreateMap {
        map,
        mapper,
        system_program: solana_program::system_program::ID,
    };
    chall
        .run_ixs_full(
            &[Instruction::new_with_bytes(
                program_id,
                &map_ix.data(),
                map_ix_accounts.to_account_metas(None)
            )],
            &[&mapper_keypair],
            &mapper,
        ).await?;

    writeln!(socket, "peppy: {}", peppy)?;
    writeln!(socket, "mapper: {}", mapper)?;
    writeln!(socket, "bn: {}", bn)?;
    writeln!(socket, "config: {}", config)?;
    writeln!(socket, "map: {}", map)?;

    // snipe shige :^)
    let bump_budget = ComputeBudgetInstruction::set_compute_unit_limit(10_000_000);
    let solve_ix = chall.read_instruction(solve_id)?;
    chall
        .run_ixs_full(&[bump_budget, solve_ix], &[&mapper_keypair], &mapper)
        .await.ok();

    let map_account = chall::Map::try_deserialize(
        &mut chall
                .ctx
                .banks_client
                .get_account(map)
                .await?
                .unwrap()
                .data()
    )?;

    if map_account.ranked {
        writeln!(socket, "congrats!")?;
        if let Ok(flag) = env::var("FLAG") {
            writeln!(socket, "flag: {:?}", flag)?;
        } else {
            writeln!(socket, "flag not found, please contact admin")?;
        }
    } else {
        writeln!(socket, "graveyarded :(")?;
    }

    Ok(())
}
