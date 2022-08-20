use std::fs;
use anyhow::{ Result as AnyResult, Error as AnyError };
use hex_literal::hex;
use serde::{ Serialize, Deserialize };
use serde_with::{ serde_as, DisplayFromStr };

use solana_sdk::{
    signer::keypair::Keypair, signature::Signer, pubkey::Pubkey, program_pack::Pack,
    system_instruction as system, message::Message, transaction::Transaction,
    instruction::{ Instruction, AccountMeta }, rent::Rent, sysvar::SysvarId,
    system_program,
};
use spl_token::{
    state::{ Mint, Account }, instruction as token,
};
use spl_associated_token_account as atoken;

use crate::*;

// 6DKhzUFaCcgYeto3sea2xPDFqQBu1Ag8Z7t8Zz9t4eT1
const MASTER_KEY: [u8; 64] = include!("../../keys/master.json");

#[derive(Clone, Debug, Default, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Accounts {
    pub player: Vec<u8>,
    pub endpoint: String,
    pub challenge_one: one::Accounts,
    pub challenge_two: two::Accounts,
    pub challenge_three: three::Accounts,
}

// NOTE these next three functions are the only place we need to add new challenges

pub async fn setup(rpc: &RpcClient) -> AnyResult<()> {
    // setup should always succeed
    one::setup(rpc).await.unwrap();
    two::setup(rpc).await.unwrap();
    three::setup(rpc).await.unwrap();

    Ok(())
}

pub async fn setup_for_player(rpc: &RpcClient, player: &Pubkey) -> AnyResult<Accounts> {
    let one_accounts = one::setup_for_player(rpc, player).await?;
    let two_accounts = two::setup_for_player(rpc, player).await?;
    let three_accounts = three::setup_for_player(rpc, player).await?;

    Ok(Accounts {
        challenge_one: one_accounts,
        challenge_two: two_accounts,
        challenge_three: three_accounts,
        ..Accounts::default()
    })
}

pub async fn check_win(rpc: &RpcClient, player: &Pubkey, challenge: u32) -> AnyResult<bool> {
    match challenge {
        1 => one::check_win(rpc, player).await,
        2 => two::check_win(rpc, player).await,
        3 => three::check_win(rpc, player).await,
        _ => Err(AnyError::msg("bad challenge")),
    }
}

async fn create_mint(rpc: &RpcClient, mint: &Keypair, authority: &Keypair, decimals: u8) -> AnyResult<()> {
    let rent = rpc.get_minimum_balance_for_rent_exemption(Mint::LEN).await?;
    let blockhash = rpc.get_latest_blockhash().await?;
    let create_ixn = system::create_account(&authority.pubkey(), &mint.pubkey(), rent, Mint::LEN as u64, &spl_token::id());
    let mint_ixn = token::initialize_mint(&spl_token::id(), &mint.pubkey(), &authority.pubkey(), None, decimals)?;

    let msg = Message::new(&[create_ixn, mint_ixn], Some(&authority.pubkey()));
    let txn = Transaction::new(&[authority, mint], msg, blockhash);

    rpc.send_and_confirm_transaction(&txn).await?;

    Ok(())
}

async fn create_account(rpc: &RpcClient, owner: &Pubkey, payer: &Keypair, mint: &Pubkey) -> AnyResult<Pubkey> {
    let blockhash = rpc.get_latest_blockhash().await?;
    #[allow(deprecated)]
    let ixn = atoken::create_associated_token_account(&payer.pubkey(), owner, mint);

    let msg = Message::new(&[ixn], Some(&payer.pubkey()));
    let txn = Transaction::new(&[payer], msg, blockhash);

    rpc.send_and_confirm_transaction(&txn).await?;

    Ok(atoken::get_associated_token_address(owner, mint))
}

async fn mint(rpc: &RpcClient, target: &Pubkey, mint: &Pubkey, authority: &Keypair, amount: u64) -> AnyResult<()> {
    let blockhash = rpc.get_latest_blockhash().await?;
    let ixn = token::mint_to(&spl_token::id(), mint, target, &authority.pubkey(), &[&authority.pubkey()], amount)?;

    let msg = Message::new(&[ixn], Some(&authority.pubkey()));
    let txn = Transaction::new(&[authority], msg, blockhash);

    rpc.send_and_confirm_transaction(&txn).await?;

    Ok(())
}

mod one {
    use super::*;

    // we furnish the player with all random pubkeys and program accounts they might need
    // the former, because they cant get them otherwise
    // the latter, for ux. they should only have to grind pdas they create as part of an attack
    // we dont provide their associated account addresses as these are trivial to get
    #[serde_as]
    #[derive(Clone, Debug, Default, Serialize, Deserialize)]
    #[serde(rename_all = "camelCase")]
    pub struct Accounts {
        #[serde_as(as = "DisplayFromStr")]
        pub program_id: Pubkey,
        #[serde_as(as = "DisplayFromStr")]
        pub satoshi: Pubkey,
        #[serde_as(as = "DisplayFromStr")]
        pub bitcoin_mint: Pubkey,
        #[serde_as(as = "DisplayFromStr")]
        pub state: Pubkey,
        #[serde_as(as = "DisplayFromStr")]
        pub deposit_account: Pubkey,
        #[serde_as(as = "DisplayFromStr")]
        pub voucher_mint: Pubkey,
    }

    // 9NK3PnfnqMihgTbNuqjWCL6t8F4kPLqSz1wuj9wYxsoh
    const PROGRAM_KEY: [u8; 64] = include!("../../keys/challenge1.json");

    // this is really annoying because i cant figure out how to use the anchor client to generate instructions
    // so im making them in js and putting the shit here. lol. cry
    const SETUP_DATA: &[u8] = &hex!("d0 99 4d 49 f2 b9 96 4e");
    const DEPOSIT_DATA: &[u8] = &hex!("f2 23 c6 89 52 e1 f2 b6 40 42 0f 00 00 00 00 00");

    const STATE: &[u8]   = b"STATE";
    const TOKEN: &[u8]   = b"TOKEN";
    const VOUCHER: &[u8] = b"VOUCHER";
    const BITCOIN_DECIMALS: u8 = 6;

    pub async fn setup(rpc: &RpcClient) -> AnyResult<()> {
        println!("challenge one setup");

        let authority = Keypair::from_bytes(&MASTER_KEY)?;
        airdrop(rpc, &authority.pubkey(), 10).await?;

        let elf = fs::read("../elf/challenge1.so")?;
        let program = Keypair::from_bytes(&PROGRAM_KEY)?;
        let _ = deploy_program(rpc, &authority, &program, &elf).await;

        Ok(())
    }

    pub async fn setup_for_player(rpc: &RpcClient, player: &Pubkey) -> AnyResult<Accounts> {
        println!("challenge one setup_for_player {}", player);

        // accounts the player needs
        let program_id = Keypair::from_bytes(&PROGRAM_KEY)?.pubkey();
        let satoshi = Keypair::new();
        let bitcoin = Keypair::new();
        let (state, _) = Pubkey::find_program_address(&[player.as_ref(), STATE], &program_id);
        let (deposit_account, _) = Pubkey::find_program_address(&[player.as_ref(), TOKEN], &program_id);
        let (voucher_mint, _) = Pubkey::find_program_address(&[player.as_ref(), VOUCHER], &program_id);

        // authority is not in play and exists to prevent player from spoofing results
        // we always airdrop so players cant sibyl to drain the payer
        let authority = Keypair::from_bytes(&MASTER_KEY)?;
        airdrop(rpc, &authority.pubkey(), 10).await?;

        // set up the bitcoin mint
        airdrop(rpc, &satoshi.pubkey(), 1).await?;
        create_mint(&rpc, &bitcoin, &satoshi, BITCOIN_DECIMALS).await?;

        // set up the program
        let setup_accounts = vec![
            AccountMeta::new_readonly(*player, false),
            AccountMeta::new(authority.pubkey(), true),
            AccountMeta::new(state, false),
            AccountMeta::new(deposit_account, false),
            AccountMeta::new_readonly(bitcoin.pubkey(), false),
            AccountMeta::new(voucher_mint, false),
            AccountMeta::new_readonly(Rent::id(), false),
            AccountMeta::new_readonly(system_program::id(), false),
            AccountMeta::new_readonly(spl_token::id(), false),
        ];
        let setup_ixn = Instruction::new_with_bytes(program_id, SETUP_DATA, setup_accounts);

        let blockhash = rpc.get_latest_blockhash().await?;
        let setup_txn = Transaction::new_signed_with_payer(
            &[setup_ixn],
            Some(&authority.pubkey()),
            &[&authority],
            blockhash,
        );

        rpc.send_and_confirm_transaction(&setup_txn).await?;

        // now create bitcoin and voucher accounts for satoshi
        let satoshi_bitcoin = create_account(rpc, &satoshi.pubkey(), &satoshi, &bitcoin.pubkey()).await?;
        let satoshi_voucher = create_account(rpc, &satoshi.pubkey(), &satoshi, &voucher_mint).await?;

        // mint
        mint(rpc, &satoshi_bitcoin, &bitcoin.pubkey(), &satoshi, 10_u64.pow(BITCOIN_DECIMALS as u32)).await?;

        // and deposit
        let deposit_accounts = vec![
            AccountMeta::new_readonly(*player, false),
            AccountMeta::new_readonly(satoshi.pubkey(), true),
            AccountMeta::new_readonly(state, false),
            AccountMeta::new(deposit_account, false),
            AccountMeta::new(voucher_mint, false),
            AccountMeta::new(satoshi_bitcoin, false),
            AccountMeta::new(satoshi_voucher, false),
            AccountMeta::new_readonly(spl_token::id(), false),
        ];
        let deposit_ixn = Instruction::new_with_bytes(program_id, DEPOSIT_DATA, deposit_accounts);

        let blockhash = rpc.get_latest_blockhash().await?;
        let deposit_txn = Transaction::new_signed_with_payer(
            &[deposit_ixn],
            Some(&satoshi.pubkey()),
            &[&satoshi],
            blockhash,
        );

        rpc.send_and_confirm_transaction(&deposit_txn).await?;

        // create accounts for the user and mint them a bitcoin
        let player_bitcoin = create_account(rpc, player, &authority, &bitcoin.pubkey()).await?;
        create_account(rpc, player, &authority, &voucher_mint).await?;
        mint(rpc, &player_bitcoin, &bitcoin.pubkey(), &satoshi, 10_u64.pow(BITCOIN_DECIMALS as u32)).await?;

        Ok(Accounts {
            program_id: program_id,
            satoshi: satoshi.pubkey(),
            bitcoin_mint: bitcoin.pubkey(),
            state: state,
            deposit_account: deposit_account,
            voucher_mint: voucher_mint,
        })
    }

    // win condition is they stole all deposited funds
    pub async fn check_win(rpc: &RpcClient, player: &Pubkey) -> AnyResult<bool> {
        let program_id = Keypair::from_bytes(&PROGRAM_KEY)?.pubkey();
        let (deposit_account, _) = Pubkey::find_program_address(&[player.as_ref(), TOKEN], &program_id);

        let account_data = rpc.get_account_data(&deposit_account).await?;
        let account = Account::unpack(&account_data)?;

        Ok(account.amount == 0)
    }
}

mod two {
    use super::*;

    // accounts for the player
    #[serde_as]
    #[derive(Clone, Debug, Default, Serialize, Deserialize)]
    #[serde(rename_all = "camelCase")]
    pub struct Accounts {
        #[serde_as(as = "DisplayFromStr")]
        pub program_id: Pubkey,
        #[serde_as(as = "DisplayFromStr")]
        pub state: Pubkey,
        #[serde_as(as = "DisplayFromStr")]
        pub wo_eth_mint: Pubkey,
        #[serde_as(as = "DisplayFromStr")]
        pub wo_eth_pool: Pubkey,
        #[serde_as(as = "DisplayFromStr")]
        pub wo_eth_pool_account: Pubkey,
        #[serde_as(as = "DisplayFromStr")]
        pub wo_eth_voucher_mint: Pubkey,
        #[serde_as(as = "DisplayFromStr")]
        pub so_eth_mint: Pubkey,
        #[serde_as(as = "DisplayFromStr")]
        pub so_eth_pool: Pubkey,
        #[serde_as(as = "DisplayFromStr")]
        pub so_eth_pool_account: Pubkey,
        #[serde_as(as = "DisplayFromStr")]
        pub so_eth_voucher_mint: Pubkey,
        #[serde_as(as = "DisplayFromStr")]
        pub st_eth_mint: Pubkey,
        #[serde_as(as = "DisplayFromStr")]
        pub st_eth_pool: Pubkey,
        #[serde_as(as = "DisplayFromStr")]
        pub st_eth_pool_account: Pubkey,
        #[serde_as(as = "DisplayFromStr")]
        pub st_eth_voucher_mint: Pubkey,
    }

    // HPyMpt2qxYjifYVkeXEGqbqX4BB4zrLj1Bw69xTTPyFn
    const PROGRAM_KEY: [u8; 64] = include!("../../keys/challenge2.json");

    // DggtXH3Vj6bP1wSsmrFoypebuvvEw1UdTL6AsmYZss86
    // BbWee59qdL445QBtjaaftca3vxKGQ5HoMPdeRpJyQ8j3
    // 9GcS1MRYo14uMLzgjxjU85THw7QE6EoBsBmM6nMLdLv1
    const WORMHOLE_KEY: [u8; 64] = include!("../../keys/wormhole_eth.json");
    const SOLLET_KEY: [u8; 64]   = include!("../../keys/sollet_eth.json");
    const LIDO_KEY: [u8; 64]     = include!("../../keys/lido_eth.json");

    const SETUP_DATA: &[u8] = &hex!("d0 99 4d 49 f2 b9 96 4e");
    const WO_POOL_DATA: &[u8] = &hex!("73 e6 d4 d3 af 31 27 a9 00");
    const SO_POOL_DATA: &[u8] = &hex!("73 e6 d4 d3 af 31 27 a9 01");
    const ST_POOL_DATA: &[u8] = &hex!("73 e6 d4 d3 af 31 27 a9 02");

    const STATE: &[u8]   = b"STATE";
    const POOL: &[u8]    = b"POOL";
    const TOKEN: &[u8]   = b"TOKEN";
    const VOUCHER: &[u8] = b"VOUCHER";

    pub async fn setup(rpc: &RpcClient) -> AnyResult<()> {
        println!("challenge two setup");

        let authority = Keypair::from_bytes(&MASTER_KEY)?;
        airdrop(rpc, &authority.pubkey(), 10).await?;

        let elf = fs::read("../elf/challenge2.so")?;
        let program = Keypair::from_bytes(&PROGRAM_KEY)?;
        let _ = deploy_program(rpc, &authority, &program, &elf).await;

        let wormhole_eth = Keypair::from_bytes(&WORMHOLE_KEY)?;
        let sollet_eth = Keypair::from_bytes(&SOLLET_KEY)?;
        let lido_eth = Keypair::from_bytes(&LIDO_KEY)?;

        let _ = create_mint(&rpc, &wormhole_eth, &authority, 8).await;
        let _ = create_mint(&rpc, &sollet_eth, &authority, 6).await;
        let _ = create_mint(&rpc, &lido_eth, &authority, 8).await;

        Ok(())
    }

    pub async fn setup_for_player(rpc: &RpcClient, player: &Pubkey) -> AnyResult<Accounts> {
        println!("challenge two setup_for_player {}", player);

        // the many, many accounts the player needs
        let program_id = Keypair::from_bytes(&PROGRAM_KEY)?.pubkey();
        let (state, _) = Pubkey::find_program_address(&[player.as_ref(), STATE], &program_id);

        let wo_eth = Keypair::from_bytes(&WORMHOLE_KEY)?.pubkey();
        let (wo_pool, _) = Pubkey::find_program_address(&[player.as_ref(), POOL, wo_eth.as_ref()], &program_id);
        let (wo_pool_account, _) = Pubkey::find_program_address(&[player.as_ref(), TOKEN, wo_eth.as_ref()], &program_id);
        let (wo_voucher_mint, _) = Pubkey::find_program_address(&[player.as_ref(), VOUCHER, wo_eth.as_ref()], &program_id);

        let so_eth = Keypair::from_bytes(&SOLLET_KEY)?.pubkey();
        let (so_pool, _) = Pubkey::find_program_address(&[player.as_ref(), POOL, so_eth.as_ref()], &program_id);
        let (so_pool_account, _) = Pubkey::find_program_address(&[player.as_ref(), TOKEN, so_eth.as_ref()], &program_id);
        let (so_voucher_mint, _) = Pubkey::find_program_address(&[player.as_ref(), VOUCHER, so_eth.as_ref()], &program_id);

        let st_eth = Keypair::from_bytes(&LIDO_KEY)?.pubkey();
        let (st_pool, _) = Pubkey::find_program_address(&[player.as_ref(), POOL, st_eth.as_ref()], &program_id);
        let (st_pool_account, _) = Pubkey::find_program_address(&[player.as_ref(), TOKEN, st_eth.as_ref()], &program_id);
        let (st_voucher_mint, _) = Pubkey::find_program_address(&[player.as_ref(), VOUCHER, st_eth.as_ref()], &program_id);

        // account they dont
        let authority = Keypair::from_bytes(&MASTER_KEY)?;
        airdrop(rpc, &authority.pubkey(), 10).await?;

        // mints are already created. theyre global for simplicity, cloned from the mainnet versions

        // set up program
        // note that add_pool requires authority as a signer
        // this means player does NOT need to call it for this challenge
        let setup_accounts = vec![
            AccountMeta::new_readonly(*player, false),
            AccountMeta::new(authority.pubkey(), true),
            AccountMeta::new(state, false),
            AccountMeta::new_readonly(Rent::id(), false),
            AccountMeta::new_readonly(system_program::id(), false),
        ];
        let setup_ixn = Instruction::new_with_bytes(program_id, SETUP_DATA, setup_accounts);

        let wo_accounts = vec![
            AccountMeta::new_readonly(*player, false),
            AccountMeta::new(authority.pubkey(), true),
            AccountMeta::new(state, false),
            AccountMeta::new_readonly(wo_eth, false),
            AccountMeta::new(wo_pool, false),
            AccountMeta::new(wo_pool_account, false),
            AccountMeta::new(wo_voucher_mint, false),
            AccountMeta::new_readonly(Rent::id(), false),
            AccountMeta::new_readonly(system_program::id(), false),
            AccountMeta::new_readonly(spl_token::id(), false),
        ];
        let wo_pool_ixn = Instruction::new_with_bytes(program_id, WO_POOL_DATA, wo_accounts.clone());

        let blockhash = rpc.get_latest_blockhash().await?;
        let setup_txn = Transaction::new_signed_with_payer(
            &[setup_ixn, wo_pool_ixn],
            Some(&authority.pubkey()),
            &[&authority],
            blockhash,
        );

        rpc.send_and_confirm_transaction(&setup_txn).await?;

        // we need two txns because of the compute budget sigh
        let mut so_accounts = wo_accounts.clone();
        so_accounts[3] = AccountMeta::new_readonly(so_eth, false);
        so_accounts[4] = AccountMeta::new(so_pool, false);
        so_accounts[5] = AccountMeta::new(so_pool_account, false);
        so_accounts[6] = AccountMeta::new(so_voucher_mint, false);
        let so_pool_ixn = Instruction::new_with_bytes(program_id, SO_POOL_DATA, so_accounts);

        let mut st_accounts = wo_accounts.clone();
        st_accounts[3] = AccountMeta::new_readonly(st_eth, false);
        st_accounts[4] = AccountMeta::new(st_pool, false);
        st_accounts[5] = AccountMeta::new(st_pool_account, false);
        st_accounts[6] = AccountMeta::new(st_voucher_mint, false);
        let st_pool_ixn = Instruction::new_with_bytes(program_id, ST_POOL_DATA, st_accounts);

        let setup_txn2 = Transaction::new_signed_with_payer(
            &[so_pool_ixn, st_pool_ixn],
            Some(&authority.pubkey()),
            &[&authority],
            blockhash,
        );

        rpc.send_and_confirm_transaction(&setup_txn2).await?;

        // put some eth in all the pools. mint directly because it doesnt matter
        // the only vouchers "in play" will be those created by the player
        mint(rpc, &wo_pool_account, &wo_eth, &authority, 100_000_000).await?;
        mint(rpc, &so_pool_account, &so_eth, &authority, 100_000_000).await?;
        mint(rpc, &st_pool_account, &st_eth, &authority, 100_000_000).await?;

        // make the player associated accounts
        let player_wo = create_account(rpc, player, &authority, &wo_eth).await?;
        let player_so = create_account(rpc, player, &authority, &so_eth).await?;
        let player_st = create_account(rpc, player, &authority, &st_eth).await?;

        // and mint the player a fractional amount of each type of eth
        mint(rpc, &player_wo, &wo_eth, &authority, 1_000).await?;
        mint(rpc, &player_so, &so_eth, &authority, 1_000).await?;
        mint(rpc, &player_st, &st_eth, &authority, 1_000).await?;

        // oh make their voucher accounts too
        create_account(rpc, player, &authority, &wo_voucher_mint).await?;
        create_account(rpc, player, &authority, &so_voucher_mint).await?;
        create_account(rpc, player, &authority, &st_voucher_mint).await?;

        Ok(Accounts{
            program_id: program_id,
            state: state,
            wo_eth_mint: wo_eth,
            wo_eth_pool: wo_pool,
            wo_eth_pool_account: wo_pool_account,
            wo_eth_voucher_mint: wo_voucher_mint,
            so_eth_mint: so_eth,
            so_eth_pool: so_pool,
            so_eth_pool_account: so_pool_account,
            so_eth_voucher_mint: so_voucher_mint,
            st_eth_mint: st_eth,
            st_eth_pool: st_pool,
            st_eth_pool_account: st_pool_account,
            st_eth_voucher_mint: st_voucher_mint,
        })
    }

    // win condition is to steal at least half of funds
    pub async fn check_win(rpc: &RpcClient, player: &Pubkey) -> AnyResult<bool> {
        let program_id = Keypair::from_bytes(&PROGRAM_KEY)?.pubkey();
        let wo_eth = Keypair::from_bytes(&WORMHOLE_KEY)?.pubkey();
        let so_eth = Keypair::from_bytes(&SOLLET_KEY)?.pubkey();
        let st_eth = Keypair::from_bytes(&LIDO_KEY)?.pubkey();

        let (wo_pool_account, _) = Pubkey::find_program_address(&[player.as_ref(), TOKEN, wo_eth.as_ref()], &program_id);
        let (so_pool_account, _) = Pubkey::find_program_address(&[player.as_ref(), TOKEN, so_eth.as_ref()], &program_id);
        let (st_pool_account, _) = Pubkey::find_program_address(&[player.as_ref(), TOKEN, st_eth.as_ref()], &program_id);

        let wo_account_data = rpc.get_account_data(&wo_pool_account).await?;
        let so_account_data = rpc.get_account_data(&so_pool_account).await?;
        let st_account_data = rpc.get_account_data(&st_pool_account).await?;

        let wo_account = Account::unpack(&wo_account_data)?;
        let so_account = Account::unpack(&so_account_data)?;
        let st_account = Account::unpack(&st_account_data)?;

        Ok(wo_account.amount + so_account.amount + st_account.amount < 150_000_000)
    }
}

mod three {
    use super::*;

    // accounts for the player
    #[serde_as]
    #[derive(Clone, Debug, Default, Serialize, Deserialize)]
    #[serde(rename_all = "camelCase")]
    pub struct Accounts {
        #[serde_as(as = "DisplayFromStr")]
        pub program_id: Pubkey,
        #[serde_as(as = "DisplayFromStr")]
        pub atomcoin_mint: Pubkey,
        #[serde_as(as = "DisplayFromStr")]
        pub state: Pubkey,
        #[serde_as(as = "DisplayFromStr")]
        pub pool: Pubkey,
        #[serde_as(as = "DisplayFromStr")]
        pub pool_account: Pubkey,
    }

    // GXU1aHkqYt7oiKa2QtifvBx1sdXE8SKmNvtww4hWMf2z
    const PROGRAM_KEY: [u8; 64] = include!("../../keys/challenge3.json");

    const SETUP_DATA: &[u8] = &hex!("d0 99 4d 49 f2 b9 96 4e");
    const ADD_POOL_DATA: &[u8] = &hex!("73 e6 d4 d3 af 31 27 a9");

    const STATE: &[u8]   = b"STATE";
    const POOL: &[u8]    = b"POOL";
    const TOKEN: &[u8]   = b"TOKEN";
    const VOUCHER: &[u8] = b"VOUCHER";
    const ATOMCOIN_DECIMALS: u8 = 0;

    pub async fn setup(rpc: &RpcClient) -> AnyResult<()> {
        println!("challenge three setup");

        let authority = Keypair::from_bytes(&MASTER_KEY)?;
        airdrop(rpc, &authority.pubkey(), 10).await?;

        let elf = fs::read("../elf/challenge3.so")?;
        let program = Keypair::from_bytes(&PROGRAM_KEY)?;
        let _ = deploy_program(rpc, &authority, &program, &elf).await;

        Ok(())
    }

    pub async fn setup_for_player(rpc: &RpcClient, player: &Pubkey) -> AnyResult<Accounts> {
        println!("challenge three setup_for_player {}", player);

        // accounts the player needs
        let program_id = Keypair::from_bytes(&PROGRAM_KEY)?.pubkey();
        let atomcoin = Keypair::new();
        let (state, _) = Pubkey::find_program_address(&[player.as_ref(), STATE], &program_id);
        let (pool, _) = Pubkey::find_program_address(&[player.as_ref(), POOL], &program_id);
        let (pool_account, _) = Pubkey::find_program_address(&[player.as_ref(), TOKEN], &program_id);

        // accounts they dont. voucher is unneeded, the entire attack is done woth borrow/repay
        let authority = Keypair::from_bytes(&MASTER_KEY)?;
        let (voucher_mint, _) = Pubkey::find_program_address(&[player.as_ref(), VOUCHER], &program_id);
        airdrop(rpc, &authority.pubkey(), 10).await?;

        // set up atomcoin mint. atomcoin is a normal token with 0 decimal for simplicity
        create_mint(&rpc, &atomcoin, &authority, ATOMCOIN_DECIMALS).await?;

        // set up program
        // this is essentially identical to the setup performed by challenge2
        let setup_accounts = vec![
            AccountMeta::new_readonly(*player, false),
            AccountMeta::new(authority.pubkey(), true),
            AccountMeta::new(state, false),
            AccountMeta::new_readonly(Rent::id(), false),
            AccountMeta::new_readonly(system_program::id(), false),
        ];
        let setup_ixn = Instruction::new_with_bytes(program_id, SETUP_DATA, setup_accounts);

        let add_pool_accounts = vec![
            AccountMeta::new_readonly(*player, false),
            AccountMeta::new(authority.pubkey(), true),
            AccountMeta::new_readonly(state, false),
            AccountMeta::new_readonly(atomcoin.pubkey(), false),
            AccountMeta::new(pool, false),
            AccountMeta::new(pool_account, false),
            AccountMeta::new(voucher_mint, false),
            AccountMeta::new_readonly(Rent::id(), false),
            AccountMeta::new_readonly(system_program::id(), false),
            AccountMeta::new_readonly(spl_token::id(), false),
        ];
        let add_pool_ixn = Instruction::new_with_bytes(program_id, ADD_POOL_DATA, add_pool_accounts);

        let blockhash = rpc.get_latest_blockhash().await?;
        let setup_txn = Transaction::new_signed_with_payer(
            &[setup_ixn, add_pool_ixn],
            Some(&authority.pubkey()),
            &[&authority],
            blockhash,
        );

        rpc.send_and_confirm_transaction(&setup_txn).await?;

        // mint 100 atomcoin directly to program because it doesnt matter
        // deposit/withdraw arent required for this challenge either
        mint(rpc, &pool_account, &atomcoin.pubkey(), &authority, 100).await?;

        // cool. create atomcoin account for player
        create_account(rpc, player, &authority, &atomcoin.pubkey()).await?;

        // note again they dont need vouchers for anything
        Ok(Accounts {
            program_id: program_id,
            atomcoin_mint: atomcoin.pubkey(),
            state: state,
            pool: pool,
            pool_account: pool_account,
        })
    }

    // win condition is to steal almost all funds
    pub async fn check_win(rpc: &RpcClient, player: &Pubkey) -> AnyResult<bool> {
        let program_id = Keypair::from_bytes(&PROGRAM_KEY)?.pubkey();
        let (pool_account, _) = Pubkey::find_program_address(&[player.as_ref(), TOKEN], &program_id);

        let account_data = rpc.get_account_data(&pool_account).await?;
        let account = Account::unpack(&account_data)?;

        Ok(account.amount <= 2)
    }
}
