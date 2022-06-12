use borsh::{
    BorshDeserialize, BorshSerialize
};
use std::{
    net::{TcpListener, TcpStream},
    error::Error,
    io::{BufReader, BufRead, Write, Read},
    str::FromStr
};
use threadpool::ThreadPool;
use tempfile::NamedTempFile;
use solana_sdk::{
    instruction::{AccountMeta, Instruction},
    transaction::Transaction,
    compute_budget
};

use solana_program::{
    pubkey::Pubkey,
    sysvar::{rent, clock},
    program_pack::Pack,
    system_program,
};
use anchor_client::solana_sdk::{
    system_instruction::{ transfer, create_account }
};
use poc_framework::{
    solana_sdk::{self, signature::Keypair, signer::Signer},
    Environment, LocalEnvironment,
};
use std::env;
use spl_token;


#[derive(BorshSerialize, BorshDeserialize)]
pub struct InitializeInstruction {
    pub opcode: u32,
    pub authority_bump: u8,
    pub sanity_bump: u8,
    pub weapon_bump: u8,
}

fn main() -> Result<(), Box<dyn Error>> {
    let listener = TcpListener::bind("0.0.0.0:8080")?;
    let pool = ThreadPool::new(4);

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        pool.execute(|| {
            handle_connection(stream);
        });
    }

    Ok(())
}

fn handle_connection(mut socket: TcpStream) -> Result<(), Box<dyn Error>> {
    let mut reader = BufReader::new(socket.try_clone().unwrap());

    let mut line = String::new();
    writeln!(socket, "length:")?;
    reader.read_line(&mut line)?;
    let len: usize = line.trim().parse()?;

    let mut solve_so = vec![0; len];
    reader.read_exact(&mut solve_so)?;

    let mut solve_file = NamedTempFile::new()?;
    solve_file.write_all(&solve_so)?;

    let mut env_builder = LocalEnvironment::builder();
    let mut env = env_builder.build();

    let program_pubkey = env.deploy_program("./darksols.so");
    let evil_contract = env.deploy_program("./evil-contract.so");
    let solve_pubkey = env.deploy_program(solve_file.path());

    let user = Keypair::new();
    let item_mint = Keypair::new();
    let item = Keypair::new();
    let item_mint_1337 = Keypair::new();
    let item_1337 = Keypair::new();

    writeln!(socket, "program pubkey: {}", program_pubkey)?;
    writeln!(socket, "solve pubkey: {}", solve_pubkey)?;
    writeln!(socket, "evil_contract pubkey: {}", evil_contract)?;
    writeln!(socket, "mint pubkey: {}", item_mint.pubkey())?;
    writeln!(socket, "item pubkey: {}", item.pubkey())?;
    writeln!(socket, "mint1337 pubkey: {}", item_mint_1337.pubkey())?;
    writeln!(socket, "item1337 pubkey: {}", item_1337.pubkey())?;
    writeln!(socket, "token pubkey: {}", spl_token::id())?;
    writeln!(socket, "user pubkey: {}", user.pubkey())?;
    writeln!(socket, "rent pubkey: {}", rent::id())?;

    let (vault, _) = Pubkey::find_program_address(&["vault".as_ref()], &program_pubkey);
    let (authority, authority_seed) = Pubkey::find_program_address(&["authority".as_ref()], &program_pubkey);
    let (sanity, sanity_seed) = Pubkey::find_program_address(&["sanity".as_ref()], &program_pubkey);
    let (weapons, weapons_seed) = Pubkey::find_program_address(&["weapon".as_ref()], &program_pubkey);

    env.create_token_mint(
        &item_mint,
        authority,
        Some(authority),
        9
    );
    env.create_token_mint(
        &item_mint_1337,
        authority,
        Some(authority),
        9
    );
    const TARGET_AMT: u64 = 50_000;
    const INIT_BAL: u64 = 20;
    const MINIMUM_BALANCE: u64 = 2_039_814;
    const VAULT_BAL: u64 = 1_000_000 + MINIMUM_BALANCE * 2;
    env.execute_as_transaction(
        &[
            transfer(
                &env.payer().pubkey(),
                &user.pubkey(),
                INIT_BAL,
            ),
            transfer(
                &env.payer().pubkey(),
                &vault,
                VAULT_BAL,
            ),
            create_account(
                &env.payer().pubkey(),
                &item.pubkey(),
                MINIMUM_BALANCE,
                spl_token::state::Account::LEN as u64,
                &spl_token::id()
            ),
            spl_token::instruction::initialize_account(
                &spl_token::id(),
                &item.pubkey(),
                &item_mint.pubkey(),
                &authority
            ).unwrap(),
            create_account(
                &env.payer().pubkey(),
                &item_1337.pubkey(),
                MINIMUM_BALANCE,
                spl_token::state::Account::LEN as u64,
                &spl_token::id()
            ),
            spl_token::instruction::initialize_account(
                &spl_token::id(),
                &item_1337.pubkey(),
                &item_mint_1337.pubkey(),
                &authority
            ).unwrap(),
            Instruction::new_with_borsh(
                program_pubkey, 
                &InitializeInstruction {
                    opcode: 0,
                    authority_bump: authority_seed,
                    sanity_bump: sanity_seed,
                    weapon_bump: weapons_seed,
                },
                vec![
                    AccountMeta::new_readonly(clock::id(), false),
                    AccountMeta::new_readonly(system_program::id(), false),
                    AccountMeta::new_readonly(spl_token::id(), false),
                    AccountMeta::new(item_mint.pubkey(), false),
                    AccountMeta::new(item.pubkey(), false),
                    AccountMeta::new(item_mint_1337.pubkey(), false),
                    AccountMeta::new(item_1337.pubkey(), false),
                    AccountMeta::new(authority, false),
                    AccountMeta::new(env.payer().pubkey(), true),
                    AccountMeta::new(sanity, false),
                    AccountMeta::new(weapons, false),
                ]
            )
        ],
        &[&env.payer(), &item, &item_1337],
    );

    // .message.serialize().len()

    line.clear();
    assert!(reader.read_line(&mut line)? != 0);
    let accts: usize = line.trim().parse()?;

    let mut metas = Vec::<AccountMeta>::new();
    for _ in 0..accts {
        line.clear();
        assert!(reader.read_line(&mut line)? != 0);

        let mut it = line.trim().split(' ');

        let meta = it.next().unwrap();
        let pubkey = Pubkey::from_str(it.next().unwrap())?;

        let is_signer = meta.contains('s');
        let is_writable = meta.contains('w');

        if is_writable {
            metas.push(AccountMeta::new(pubkey, is_signer));
        } else {
            metas.push(AccountMeta::new_readonly(pubkey, is_signer));
        }

    }

    line.clear();
    assert!(reader.read_line(&mut line)? != 0);
    let ix_data_len: usize = line.trim().parse()?;
    let mut ix_data = vec![0; ix_data_len];

    reader.read_exact(&mut ix_data)?;

    let ix = Instruction::new_with_bytes(
        solve_pubkey,
        &ix_data,
        metas.to_vec()
    );

    let tx = Transaction::new_signed_with_payer(
        &[
            compute_budget::request_units(500_000),
            ix
        ],
        Some(&user.pubkey()),
        &vec![&user],
        env.get_recent_blockhash(),
    );

    env.execute_transaction(tx);
    let user_bal = env.get_account(user.pubkey()).unwrap().lamports;
    writeln!(socket, "user bal: {:?}", user_bal)?;
    writeln!(socket, "vault bal: {:?}", env.get_account(vault).unwrap().lamports)?;

    if user_bal > TARGET_AMT {
        writeln!(socket, "congrats!")?;
        if let Ok(flag) = env::var("FLAG") {
            writeln!(socket, "flag: {:?}", flag)?;
        } else {
            writeln!(socket, "flag not found, please contact admin")?;
        }
    }

    Ok(())
}
