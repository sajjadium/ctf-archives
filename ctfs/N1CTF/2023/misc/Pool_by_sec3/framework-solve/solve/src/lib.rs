use solana_program::entrypoint;

pub mod processor;
use processor::process_instruction;

solana_program::declare_id!("28prS7e14Fsm97GE5ws2YpjxseFNkiA33tB5D3hLZv3t");

entrypoint!(process_instruction);