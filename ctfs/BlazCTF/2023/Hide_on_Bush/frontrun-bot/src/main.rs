use std::sync::Arc;

use anyhow::Result;
use artemis_core::collectors::mempool_collector::MempoolCollector;
use artemis_core::engine::Engine;
use clap::Parser;
use ethers::{
    prelude::MiddlewareBuilder,
    providers::{Provider, Ws},
    signers::{LocalWallet, Signer},
    types::Address,
};
use ethers::middleware::Middleware;
use tracing::Level;
use tracing_subscriber::{filter, prelude::*};

use crate::frontrun_strategy::FrontRunStrategy;
use crate::mempool_executor::MempoolExecutor;

mod frontrun_strategy;
mod utils;
mod call_tracer;
mod mempool_executor;

#[derive(Parser, Debug)]
pub struct Args {
    pub ws: String,
    pub private_key: String,
    pub contract_address: Address,
    pub weth_address: Address,
}

#[tokio::main]
async fn main() -> Result<()> {
    let filter = filter::Targets::new()
        .with_target("frontrun_bot", Level::TRACE)
        .with_target("artemis_core", Level::INFO);

    tracing_subscriber::registry()
        .with(tracing_subscriber::fmt::layer())
        .with(filter)
        .init();

    tracing::info!("hi");

    let args = Args::parse();

    let ws = Ws::connect_with_reconnects(args.ws, 10).await?;
    let provider = Provider::new(ws);
    let chain_id = provider.get_chainid().await?.as_u64();

    let wallet: LocalWallet = args.private_key.parse().unwrap();
    let wallet = wallet.with_chain_id(chain_id);
    let address = wallet.address();

    let provider_with_nonce_manager = Arc::new(provider.clone().nonce_manager(address).with_signer(wallet.clone()));

    let mut engine = Engine::default();

    engine.add_collector(Box::new(MempoolCollector::new(Arc::new(provider.clone()))));
    engine.add_strategy(Box::new(FrontRunStrategy {
        bot_address: utils::eaddress_to_raddress(&args.contract_address),
        weth_address: utils::eaddress_to_raddress(&args.weth_address),
        sender_address: utils::eaddress_to_raddress(&address),
        provider: Arc::new(provider.clone()),
    }));
    engine.add_executor(Box::new(MempoolExecutor::new(provider_with_nonce_manager)));

    if let Ok(mut set) = engine.run().await {
        while let Some(res) = set.join_next().await {
            tracing::info!("res: {:?}", res);
        }
    }

    Ok(())
}