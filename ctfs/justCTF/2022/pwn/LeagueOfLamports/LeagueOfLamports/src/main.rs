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
};

use solana_program::{
    pubkey::Pubkey
};
use anchor_client::solana_sdk::system_instruction::transfer;
use poc_framework::{
    solana_sdk::{self, signature::Keypair, signer::Signer},
    Environment, LocalEnvironment,
    /*
     * LOGGING CODE BEG
     * 
     * LogLevel, PrintableTransaction,
     * setup_logging
     *
     * LOGGING CODE END
     */
};
use std::env;

fn main() -> Result<(), Box<dyn Error>> {
    let listener = TcpListener::bind("0.0.0.0:8080")?;
    let pool = ThreadPool::new(4);

    /*
     * LOGGING CODE BEG
     *
     * setup_logging(LogLevel::DEBUG);
     *
     * LOGGING CODE END
     */

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
    writeln!(socket, "length: ")?;
    reader.read_line(&mut line)?;
    let len: usize = line.trim().parse()?;

    let mut solve_so = vec![0; len];
    reader.read_exact(&mut solve_so)?;

    let mut solve_file = NamedTempFile::new()?;
    solve_file.write_all(&solve_so)?;

    let mut env_builder = LocalEnvironment::builder();
    let mut env = env_builder.build();

    let program_pubkey = env.deploy_program("./leagueoflamports.so");
    let solve_pubkey = env.deploy_program(solve_file.path());

    let user = Keypair::new();

    writeln!(socket, "program pubkey: {}", program_pubkey)?;
    writeln!(socket, "solve pubkey: {}", solve_pubkey)?;
    writeln!(socket, "user pubkey: {}", user.pubkey())?;

    let (vault, _) = Pubkey::find_program_address(&["vault".as_ref()], &program_pubkey);

    const TARGET_AMT: u64 = 50_000;
    const INIT_BAL: u64 = 10;
    const VAULT_BAL: u64 = 1_000_000;
    env.execute_as_transaction(
        &[transfer(
            &env.payer().pubkey(),
            &user.pubkey(),
            INIT_BAL,
        ),
        transfer(
            &env.payer().pubkey(),
            &vault,
            VAULT_BAL,
        )
        ],
        &[&env.payer()],
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
        metas
    );

    let tx = Transaction::new_signed_with_payer(
        &[ix],
        Some(&user.pubkey()),
        &vec![&user],
        env.get_recent_blockhash(),
    );

    /*
     * LOGGING CODE BEG
     * uncomment #153, comment #157
     *
     * env.execute_transaction(tx).print();
     *
     * LOGGING CODE END
     */
    env.execute_transaction(tx); // comment this line if you uncommented line 153
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
