use tokio::time::{ sleep, Duration };
use anyhow::{ Result as AnyResult, Error as AnyError };

use solana_sdk::{
    signer::keypair::Keypair, signature::{Signer, Signature},
    pubkey::Pubkey, native_token::LAMPORTS_PER_SOL,
    bpf_loader_upgradeable::{ self as loader, UpgradeableLoaderState },
    message::Message, transaction::Transaction, packet::PACKET_DATA_SIZE,
    hash::Hash, commitment_config::CommitmentConfig,
};
use solana_client::{
    nonblocking::rpc_client::RpcClient, rpc_response::Response,
};

pub mod challenge;

const RPC_URL: &str = "http://127.0.0.1:8899";

pub fn rpc() -> RpcClient {
    RpcClient::new_with_commitment(RPC_URL.to_string(), commit())
}

pub fn commit() -> CommitmentConfig {
    CommitmentConfig::confirmed()
}

pub async fn airdrop(rpc: &RpcClient, target: &Pubkey, amount: u64) -> AnyResult<()> {
    let sig = rpc.request_airdrop(target, amount.saturating_mul(LAMPORTS_PER_SOL)).await?;
    rpc.poll_for_signature(&sig).await?;

    Ok(())
}

pub async fn make_new_player(rpc: &RpcClient, url: &str) -> AnyResult<challenge::Accounts> {
    let player = Keypair::new();
    airdrop(&rpc, &player.pubkey(), 100).await?;

    let mut accounts = challenge::setup_for_player(&rpc, &player.pubkey()).await?;
    accounts.player = player.to_bytes().to_vec();
    accounts.endpoint = format!("{}/{}", url, player.pubkey().to_string());

    Ok(accounts)
}

// i cant believe i have to do this myself
pub async fn deploy_program(
    rpc: &RpcClient,
    authority: &Keypair,
    program: &Keypair,
    elf: &[u8],
) -> AnyResult<()> {
    // first check if this address has already been deployed to
    // eg, challenge programs when restarting the server
    if let Ok(Response { value: None, .. }) = rpc.get_account_with_commitment(&program.pubkey(), commit()).await {
        println!("deploying {}kb program to address {}", elf.len() / 1024, program.pubkey());
    }
    else {
        println!("skipping {}: program has already been deployed", program.pubkey());
        return Err(AnyError::msg("program already deployed"));
    }

    // alright cool get a new buffer address
    // programdata is a pda and the instruction builder handles it
    let buffer = Keypair::new();

    // we need three accounts. get the rent numbers for them
    // program is a fixed size so it does the rent for this automatically i think?
    // i havent read the instruction data but i never need to pass it in
    let elf_len = elf.len();
    let programdata_len = UpgradeableLoaderState::size_of_programdata(elf_len);
    let buffer_len = UpgradeableLoaderState::size_of_buffer(elf_len);

    let programdata_rent = rpc.get_minimum_balance_for_rent_exemption(programdata_len).await?;
    let buffer_rent = rpc.get_minimum_balance_for_rent_exemption(buffer_len).await?;

    // now the way this goes is we need to:
    // * create buffer
    // * memcpy to buffer
    // * deploy from buffer
    // * close buffer

    // first, create
    let create_ixns = loader::create_buffer(
        &authority.pubkey(),
        &buffer.pubkey(),
        &authority.pubkey(),
        buffer_rent,
        elf_len,
    )?;

    let blockhash = rpc.get_latest_blockhash().await?;
    let create_txn = Transaction::new_signed_with_payer(
        &create_ixns,
        Some(&authority.pubkey()),
        &[authority, &buffer],
        blockhash,
    );

    rpc.send_and_confirm_transaction(&create_txn).await?;

    // next, write. this shit is annoying
    // actually jk its mostly stolen haha thanks starry
    let mk_write_msg = |bytes: Vec<u8>, offset: u32, blockhash: &Hash| {
        let ixn = loader::write(&buffer.pubkey(), &authority.pubkey(), offset, bytes);
        Message::new_with_blockhash(&[ixn], Some(&authority.pubkey()), &blockhash)
    };

    // technically this could simplify to a constant but whatever
    let empty_write_msg = mk_write_msg(Vec::new(), 0, &blockhash);
    let txn_size = bincode::serialized_size(&Transaction {
        signatures: vec![
            Signature::default();
            empty_write_msg.header.num_required_signatures as usize
        ],
        message: empty_write_msg,
    })? as usize;
    let data_chunk_size = PACKET_DATA_SIZE - txn_size - 1;

    // alright go time
    let write_chunks: Vec<&[u8]> = elf.chunks(data_chunk_size).collect();
    let mut write_sigs: Vec<Signature> = Vec::new();
    write_sigs.resize(write_chunks.len(), Signature::default());

    // first we spam everything once
    for (i, chunk) in write_chunks.iter().enumerate() {
        let write_txn = Transaction::new(
            &[authority],
            mk_write_msg(chunk.to_vec(), (i * data_chunk_size) as u32, &blockhash),
            blockhash,
        );

        write_sigs[i] = rpc.send_transaction(&write_txn).await?;
        sleep(Duration::from_millis(1)).await;
    }

    // now we confirm them all and retry if needed
    for (i, sig) in write_sigs.iter().enumerate() {
        if let Err(_) = rpc.poll_for_signature(&sig).await {
            let blockhash = rpc.get_latest_blockhash().await?;
            rpc.send_and_confirm_transaction(&Transaction::new(
                &[authority],
                mk_write_msg(write_chunks[i].to_vec(), (i * data_chunk_size) as u32, &blockhash),
                blockhash,
            )).await?;
        }
    }

    // finally the deploy transaction
    // im 80% sure this frees the buffer actually
    let deploy_ixns = loader::deploy_with_max_program_len(
        &authority.pubkey(),
        &program.pubkey(),
        &buffer.pubkey(),
        &authority.pubkey(),
        programdata_rent,
        elf_len,
    )?;

    let blockhash = rpc.get_latest_blockhash().await?;
    let deploy_txn = Transaction::new_signed_with_payer(
        &deploy_ixns,
        Some(&authority.pubkey()),
        &[authority, program],
        blockhash,
    );

    rpc.send_and_confirm_transaction(&deploy_txn).await?;

    // wow! all done
    Ok(())
}
