use revm::{Database, EVMData, Inspector};
use revm::interpreter::{CallInputs, CallScheme, CreateInputs, Gas, InstructionResult};
use revm::precompile::Bytes;
use revm::primitives::{Address, U256};

pub struct Call {
    pub delegate_call: bool,
    pub to: Address,
    pub data: Bytes,
    pub value: U256,
}

#[derive(Default)]
pub struct CallTracer {
    pub depth: usize,
    pub top_level_calls: Vec<Call>,
}

impl<DB: Database> Inspector<DB> for CallTracer {
    fn call(
        &mut self,
        _data: &mut EVMData<'_, DB>,
        inputs: &mut CallInputs,
    ) -> (InstructionResult, Gas, Bytes) {
        if self.depth == 1 && (inputs.context.scheme == CallScheme::Call || inputs.context.scheme == CallScheme::DelegateCall) {
            let is_delegate_call = inputs.context.scheme == CallScheme::DelegateCall;
            let to = inputs.contract;
            let data = inputs.input.clone();
            let value = inputs.context.apparent_value;

            self.top_level_calls.push(Call {
                delegate_call: is_delegate_call,
                to,
                data,
                value,
            });
        }

        self.depth += 1;
        (InstructionResult::Continue, Gas::new(0), Bytes::new())
    }

    fn call_end(
        &mut self,
        _data: &mut EVMData<'_, DB>,
        _inputs: &CallInputs,
        remaining_gas: Gas,
        ret: InstructionResult,
        out: Bytes,
    ) -> (InstructionResult, Gas, Bytes) {
        self.depth -= 1;
        (ret, remaining_gas, out)
    }

    fn create(
        &mut self,
        _data: &mut EVMData<'_, DB>,
        _inputs: &mut CreateInputs,
    ) -> (InstructionResult, Option<Address>, Gas, Bytes) {
        self.depth += 1;
        (
            InstructionResult::Continue,
            None,
            Gas::new(0),
            Bytes::default(),
        )
    }

    fn create_end(
        &mut self,
        _data: &mut EVMData<'_, DB>,
        _inputs: &CreateInputs,
        ret: InstructionResult,
        address: Option<Address>,
        remaining_gas: Gas,
        out: Bytes,
    ) -> (InstructionResult, Option<Address>, Gas, Bytes) {
        self.depth -= 1;
        (ret, address, remaining_gas, out)
    }

    /// Called when a contract has been self-destructed with funds transferred to target.
    fn selfdestruct(&mut self, _contract: Address, _target: Address, _value: U256) {}
}