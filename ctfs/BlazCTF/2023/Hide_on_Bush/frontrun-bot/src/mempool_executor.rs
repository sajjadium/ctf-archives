use std::{
    ops::{Div, Mul},
    sync::Arc,
};

use anyhow::{Context, Result};
use artemis_core::executors::mempool_executor::SubmitTxToMempool;
use artemis_core::types::Executor;
use async_trait::async_trait;
use ethers::providers::Middleware;

pub struct MempoolExecutor<M> {
    client: Arc<M>,
}

impl<M: Middleware> MempoolExecutor<M> {
    pub fn new(client: Arc<M>) -> Self {
        Self { client }
    }
}

#[async_trait]
impl<M> Executor<SubmitTxToMempool> for MempoolExecutor<M>
    where
        M: Middleware,
        M::Error: 'static,
{
    /// Send a transaction to the mempool.
    async fn execute(&self, mut action: SubmitTxToMempool) -> Result<()> {
        let gas_usage = action.tx.gas().unwrap().as_u64();

        let bid_gas_price = if let Some(gas_bid_info) = action.gas_bid_info {
            let breakeven_gas_price = gas_bid_info.total_profit / gas_usage;
            breakeven_gas_price
                .mul(gas_bid_info.bid_percentage)
                .div(100)
        } else {
            self
                .client
                .get_gas_price()
                .await
                .context("Error getting gas price: {}")?
        };

        action.tx.set_gas_price(bid_gas_price);

        tracing::info!("sending tx with gas price {}", bid_gas_price);

        self.client.send_transaction(action.tx, None).await?;
        Ok(())
    }
}
