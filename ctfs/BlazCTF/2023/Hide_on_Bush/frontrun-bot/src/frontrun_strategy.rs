use std::collections::HashMap;
use std::sync::Arc;

use artemis_core::executors::mempool_executor::{GasBidInfo, SubmitTxToMempool};
use artemis_core::types::Strategy;
use async_trait::async_trait;
use ethers::abi::{Bytes, ethereum_types, Token};
use ethers::prelude::{Block, BlockId, H256, Middleware, TransactionRequest, TxHash};
use ethers::prelude::transaction::eip2718::TypedTransaction;
use ethers::types::Transaction;
use revm::db::EthersDB;
use revm::EVM;
use revm::inspectors::NoOpInspector;
use revm::primitives::{Address, B256, b256, CreateScheme, EVMResult, ExecutionResult, hex, Log, SpecId, TransactTo, U256};
use revm::primitives::alloy_primitives::I256;

use crate::{call_tracer, utils};
use crate::call_tracer::CallTracer;

const ERC20_TRANSFER_TOPIC: B256 = b256!("ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef");
const WETH_WITHDRAWAL_TOPIC: B256 = b256!("7fcf532c15f0a6db0bd6d0e038bea71d30d808c7d98cb3bf7268a95bf5081b65");
const WETH_DEPOSIT_TOPIC: B256 = b256!("e1fffcc4923d04b559f4d29a8bfc6cda04eb5b0d3c460751c2402c5c5cc9109c");


pub struct FrontRunStrategy<M: Middleware> {
    pub bot_address: Address,
    pub weth_address: Address,
    pub sender_address: Address,
    pub provider: Arc<M>,
}

impl<M> FrontRunStrategy<M>
    where M: Middleware + 'static
{
    async fn process_tx(&mut self, tx: Transaction) -> anyhow::Result<Option<SubmitTxToMempool>> {
        let block_number = self.provider.get_block_number().await
            .map_err(|err| anyhow::anyhow!("Failed to get block number: {:?}", err))?;

        let block = self.provider.get_block(BlockId::Number(block_number.into())).await
            .map_err(|err| anyhow::anyhow!("Failed to get block {}: {:?}", block_number, err))?
            .ok_or_else(|| anyhow::anyhow!("Block not found"))?;

        let (top_call_recorder, evm_result) = self.simulate_tx(&tx, &block)?;
        let (balance_changes, _) = self.process_evm_result(&evm_result);
        let sender_profit = balance_changes.get(&utils::eaddress_to_raddress(&tx.from)).unwrap_or(&I256::ZERO);
        tracing::info!("sender profit: {:?}", sender_profit);

        if sender_profit.is_negative() || sender_profit.is_zero() {
            return Ok(None);
        }

        let mut replacements = HashMap::new();
        replacements.insert(utils::eaddress_to_raddress(&tx.from), self.sender_address);
        replacements.insert(utils::eaddress_to_raddress(&tx.to.unwrap()), self.bot_address);

        let mut evm = self.new_evm_with_ethers_db(&block)?;
        evm.env.tx.caller = self.sender_address;
        evm.env.tx.gas_limit = utils::u256_to_u64(&evm.env.block.gas_limit);
        evm.env.tx.transact_to = TransactTo::Call(self.bot_address);
        evm.env.tx.value = Default::default();
        evm.env.tx.data = calls_to_calldata(&top_call_recorder.top_level_calls, &replacements);
        tracing::debug!("reconstructed payload: {:#x}", evm.env.tx.data);

        let evm_result = std::thread::spawn(move || evm.inspect(&mut NoOpInspector {}))
            .join()
            .map_err(|err| anyhow::anyhow!("Failed to inspect tx: {:?}", err))?;

        let (balance_changes, gas_used) = self.process_evm_result(&evm_result);
        let replay_profit = balance_changes.get(&self.sender_address).unwrap_or(&I256::ZERO);
        tracing::info!("replay profit: {:?}", replay_profit);

        if replay_profit.is_negative() || replay_profit.is_zero() {
            return Ok(None);
        }

        let replay_profit = replay_profit.abs().into_raw();
        let chain_id = self.provider.get_chainid().await?.as_u64();


        Ok(Some(SubmitTxToMempool {
            tx: TypedTransaction::Legacy(
                TransactionRequest::new()
                    .from(utils::raddress_to_eaddress(&self.sender_address))
                    .to(utils::raddress_to_eaddress(&self.bot_address))
                    .data(calls_to_calldata(&top_call_recorder.top_level_calls, &replacements).to_vec())
                    .chain_id(chain_id)
                    .gas(gas_used * 150 / 100),
            ),
            gas_bid_info: Some(GasBidInfo {
                total_profit: utils::ru256_to_eu256(&replay_profit),
                bid_percentage: 10,
            }),
        }))
    }

    fn new_evm_with_ethers_db(&mut self, block: &Block<H256>) -> anyhow::Result<EVM<EthersDB<M>>> {
        let block_number = block.number.ok_or_else(|| anyhow::anyhow!("Block number not found"))?;
        let ethers_db = EthersDB::new(self.provider.clone(), Some(block_number.into()))
            .ok_or_else(|| anyhow::anyhow!("Failed to create EthersDB"))?;

        let mut evm = EVM::new();
        evm.database(ethers_db);

        evm.env.cfg.spec_id = SpecId::LATEST;
        evm.env.cfg.disable_base_fee = true;
        update_revm_block_from_ethers_block(&mut evm.env.block, block);

        Ok(evm)
    }

    fn simulate_tx(&mut self, tx: &Transaction, block: &Block<H256>) -> anyhow::Result<(Box<CallTracer>, EVMResult<()>)> {
        let mut evm = self.new_evm_with_ethers_db(block)?;

        update_revm_tx_from_ethers_tx(&mut evm.env.tx, &tx);

        let mut top_call_recorder = Box::<CallTracer>::default();

        let evm_result = {
            std::thread::spawn(move || {
                let result = evm.inspect(&mut top_call_recorder);
                (top_call_recorder, result)
            })
                .join()
                .map_err(|err| anyhow::anyhow!("Failed to inspect tx: {:?}", err))?
        };

        Ok(evm_result)
    }

    fn process_evm_result(&self, evm_result: &EVMResult<()>) -> (HashMap<Address, I256>, u64) {
        let (logs, gas) = match evm_result {
            Ok(result) => match &result.result {
                ExecutionResult::Success { logs, gas_used, .. } => (Some(logs), gas_used),
                ExecutionResult::Revert { gas_used, .. } => (None, gas_used),
                ExecutionResult::Halt { gas_used, .. } => (None, gas_used),
            }
            Err(_) => (None, &0u64),
        };

        match logs {
            Some(logs) => (get_balance_changes_from_logs(&logs, &self.weth_address), *gas),
            None => (HashMap::new(), *gas),
        }
    }
}

#[async_trait]
impl<M> Strategy<Transaction, SubmitTxToMempool> for FrontRunStrategy<M>
    where M: Middleware + 'static
{
    async fn sync_state(&mut self) -> anyhow::Result<()> {
        Ok(())
    }

    async fn process_event(&mut self, event: Transaction) -> Vec<SubmitTxToMempool> {
        if event.from.0 == self.sender_address.0 {
            return vec![];
        }

        if event.to.is_none() {
            return vec![];
        }

        tracing::info!("received tx: {:?}", event);

        let result = self.process_tx(event).await;

        match result {
            Ok(Some(tx)) => vec![tx],
            Ok(None) => vec![],
            Err(err) => {
                tracing::error!("Error processing tx: {:?}", err);
                vec![]
            }
        }
    }
}

fn update_revm_block_from_ethers_block(r_block: &mut revm::primitives::BlockEnv, block: &Block<TxHash>) {
    r_block.number = utils::u64_to_ru256(block.number.unwrap().as_u64() + 1);
    r_block.coinbase = utils::eaddress_to_raddress(&block.author.unwrap_or_default());
    r_block.timestamp = utils::u64_to_ru256(block.timestamp.as_u64());
    r_block.gas_limit = utils::u64_to_ru256(block.gas_limit.as_u64());
}

fn update_revm_tx_from_ethers_tx(r_tx: &mut revm::primitives::TxEnv, tx: &Transaction) {
    r_tx.caller = utils::eaddress_to_raddress(&tx.from);
    r_tx.gas_limit = tx.gas.as_u64();
    r_tx.gas_price = Default::default();
    r_tx.transact_to = match tx.to {
        Some(to) => TransactTo::Call(utils::eaddress_to_raddress(&to)),
        None => TransactTo::Create(CreateScheme::Create),
    };
    r_tx.value = utils::eu256_to_ru256(&tx.value);
    r_tx.data = tx.input.to_vec().into();
}

fn get_balance_changes_from_logs(logs: &[revm::primitives::Log], weth_address: &Address) -> HashMap<Address, I256> {
    let mut balance_changes = HashMap::new();

    logs.iter().filter(|log| log.address.eq(weth_address)).for_each(|log| {
        tracing::debug!("log: {:?}", log);

        let (from, to, value) = match log.topics.as_slice() {
            [ERC20_TRANSFER_TOPIC, from, to] => {
                let from = Address::from_slice(&from.0[12..]);
                let to = Address::from_slice(&to.0[12..]);
                let value = revm::primitives::U256::from_be_bytes::<32>(log.data[..32].try_into().unwrap());
                (from, to, value)
            }
            [WETH_WITHDRAWAL_TOPIC, from] => {
                let from = Address::from_slice(&from.0[12..]);
                let value = revm::primitives::U256::from_be_bytes::<32>(log.data[..32].try_into().unwrap());
                (from, Address::default(), value)
            }
            [WETH_DEPOSIT_TOPIC, to] => {
                let to = Address::from_slice(&to.0[12..]);
                let value = revm::primitives::U256::from_be_bytes::<32>(log.data[..32].try_into().unwrap());
                (Address::default(), to, value)
            }
            _ => return,
        };

        let value = I256::from_raw(value);

        tracing::debug!("from: {:?}, to: {:?}, value: {:?}", from, to, value);

        balance_changes.entry(from).and_modify(|v| *v -= value).or_insert(-value);
        balance_changes.entry(to).and_modify(|v| *v += value).or_insert(value);
    });

    balance_changes.retain(|_, v| !v.is_zero());
    balance_changes
}

fn calls_to_calldata(calls: &[call_tracer::Call], replacements: &HashMap<Address, Address>) -> revm::primitives::Bytes {
    // cast sig "approve(address, uint256)"
    const APPROVE_SIG: [u8; 4] = hex!("095ea7b3");

    // cast sig "go(bytes[] calldata data)"
    const GO_SIG: [u8; 4] = hex!("73d78389");

    let approval_to_clear = calls
        .iter()
        .filter_map(|call| {
            if call.data.len() == 4 + 32 + 32 && call.data[0..4] == APPROVE_SIG {
                let spender = Address::from_slice(&call.data[16..36]);
                Some((call.to, spender))
            } else {
                None
            }
        })
        .map(|(token, spender)| {
            let cd = APPROVE_SIG
                .iter()
                .copied()
                .chain([0u8; 12].iter().copied())
                .chain(spender.iter().copied())
                .chain(U256::ZERO.to_be_bytes::<32>().iter().copied())
                .collect::<Vec<_>>();

            encode_action(false, token, U256::ZERO, cd.into())
        });

    let calls = calls
        .iter()
        .map(|call| {
            let mut data = call.data.to_vec();
            replace_addresses(&mut data, replacements);

            encode_action(call.delegate_call, call.to, call.value, data.into())
        })
        .chain(approval_to_clear)
        .collect();

    GO_SIG
        .iter()
        .copied()
        .chain(ethers::abi::encode(&[Token::Array(calls)]).drain(..))
        .collect::<Vec<_>>()
        .into()
}

fn encode_action(is_delegate_call: bool, to: Address, value: U256, data: Bytes) -> Token {
    Token::Bytes(ethers::abi::encode(&[
        Token::Bool(is_delegate_call),
        Token::Address(ethereum_types::Address::from(to.0.0)),
        Token::Uint(value.to_be_bytes::<32>()[..].into()),
        Token::Bytes(data),
    ]))
}

fn replace_addresses(data: &mut Vec<u8>, replacements: &HashMap<Address, Address>) {
    let mut index = 0;
    let len = data.len();

    while index + 20 <= len {
        let address = Address::from_slice(&data[index..index + 20]);
        if let Some(replacement) = replacements.get(&address) {
            data.splice(index..index + 20, replacement.as_slice().iter().copied());
            index += 20;
        } else {
            index += 1;
        }
    }
}