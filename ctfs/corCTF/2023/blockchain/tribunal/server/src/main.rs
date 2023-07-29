use std::env;
use std::io::Write;

use sol_ctf_framework::ChallengeBuilder;

use solana_program::{
    instruction::{AccountMeta, Instruction},
    pubkey::Pubkey,
    system_instruction, system_program,
};
use solana_program_test::tokio;
use solana_sdk::{signature::Signer, signer::keypair::Keypair};
use std::error::Error;

use std::net::{TcpListener, TcpStream};

#[derive(borsh::BorshSerialize)]
pub enum TribunalInstruction {
    Initialize { config_bump: u8, vault_bump: u8 },
    Propose { proposal_id: u8, proposal_bump: u8 },
    Vote { proposal_id: u8, amount: u64 },
    Withdraw { amount: u64 },
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let listener = TcpListener::bind("0.0.0.0:8080")?;

    println!("starting server at port 8080");

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
    writeln!(socket, "tribunal")?;
    writeln!(socket, "{}", std::fs::read_to_string("art.txt")?)?; // just some fun ANSI art
    writeln!(
        socket,
        "there's been some drama in our ctf team recently..."
    )?;
    writeln!(socket, "the cor tribunal will take care of it.")?;
    writeln!(
        socket,
        "as a member of the jury, what do you think we need to deal with first?"
    )?;
    writeln!(socket, "proposal 1: depose supreme dicator FizzBuzz101")?;
    writeln!(
        socket,
        "proposal 2: send chop0 to the gulags for not writing a challenge"
    )?;
    writeln!(socket, "proposal 3: the web mafia unionizes")?;
    writeln!(
        socket,
        "proposal 4: depose Fizz AND the web mafia unionizes"
    )?;
    writeln!(
        socket,
        "proposal 5: start a revolt and break away from dicegang"
    )?;

    writeln!(socket, "\nnow, vote for your choice...\n")?;

    let mut builder = ChallengeBuilder::try_from(socket.try_clone().unwrap()).unwrap();

    // load program
    let program_id = builder.add_program("./tribunal.so", None);
    let solve_id = builder.input_program()?;

    let mut chall = builder.build().await;

    // get access to funds from ctf framework
    let payer_keypair = &chall.ctx.payer;
    let payer = payer_keypair.pubkey();

    // create admin user
    let admin_keypair = Keypair::new();
    let admin = admin_keypair.pubkey();

    // fund admin user
    chall
        .run_ix(system_instruction::transfer(
            &payer,
            &admin,
            100_000_000_000, // 100 sol
        ))
        .await?;

    // create user
    let user_keypair = Keypair::new();
    let user = user_keypair.pubkey();

    // fund user
    chall
        .run_ix(system_instruction::transfer(&payer, &user, 1_000_000_000)) // 1 sol
        .await?;

    writeln!(socket, "\nsome information for you:")?;
    writeln!(socket, "program: {}", program_id)?;
    writeln!(socket, "user: {}", user)?;

    let (config_addr, config_bump) =
        Pubkey::find_program_address(&["CONFIG".as_bytes()], &program_id);
    let (vault_addr, vault_bump) = Pubkey::find_program_address(&["VAULT".as_bytes()], &program_id);

    // start the tribunal
    let mut ixs = vec![Instruction::new_with_borsh(
        program_id,
        &TribunalInstruction::Initialize {
            config_bump,
            vault_bump,
        },
        vec![
            AccountMeta::new(admin, true),
            AccountMeta::new(config_addr, false),
            AccountMeta::new(vault_addr, false),
            AccountMeta::new_readonly(system_program::id(), false),
        ],
    )];

    // create the five proposals
    for i in 1..=5_u8 {
        let (addr, bump) =
            Pubkey::find_program_address(&["PROPOSAL".as_bytes(), &i.to_be_bytes()], &program_id);
        ixs.push(Instruction::new_with_borsh(
            program_id,
            &TribunalInstruction::Propose {
                proposal_id: i,
                proposal_bump: bump,
            },
            vec![
                AccountMeta::new(admin, true),
                AccountMeta::new(config_addr, false),
                AccountMeta::new(addr, false),
                AccountMeta::new_readonly(system_program::id(), false),
            ],
        ));
    }

    // personally, down with fizz and the web union will rise!!
    let (p4_addr, _) =
            Pubkey::find_program_address(&["PROPOSAL".as_bytes(), &4_u8.to_be_bytes()], &program_id);
    ixs.push(Instruction::new_with_borsh(
        program_id,
        &TribunalInstruction::Vote {
            proposal_id: 4,
            amount: 99_000_000_000, // 99 sol
        },
        vec![
            AccountMeta::new(admin, true),
            AccountMeta::new(config_addr, false),
            AccountMeta::new(vault_addr, false),
            AccountMeta::new(p4_addr, false),
            AccountMeta::new_readonly(system_program::id(), false),
        ],
    ));

    // run setup instructions
    chall
        .run_ixs_full(&ixs, &[&admin_keypair], &admin_keypair.pubkey())
        .await?;

    let solve_ix = chall.read_instruction(solve_id)?;
    chall
        .run_ixs_full(&[solve_ix], &[&user_keypair], &user_keypair.pubkey())
        .await?;

    if let Some(account) = chall.ctx.banks_client.get_account(user).await? {
        writeln!(socket, "lamports after exploit: {:?}", account.lamports)?;

        // 90 sol
        if account.lamports > 90_000_000_000 {
            writeln!(socket, "you'll be the focus of the next tribunal...")?;
            writeln!(
                socket,
                "flag: {}",
                env::var("FLAG").unwrap_or_else(|_| "corctf{test_flag}".to_string())
            )?;
        }
    } else {
        writeln!(socket, "there was an error reading the user's balance")?;
    }

    Ok(())
}
