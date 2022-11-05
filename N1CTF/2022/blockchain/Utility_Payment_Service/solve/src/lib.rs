use solana_program::entrypoint;

pub mod processor;
use processor::process_instruction;
entrypoint!(process_instruction);
