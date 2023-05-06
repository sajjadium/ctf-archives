#![allow(clippy::integer_arithmetic)]
#![allow(clippy::upper_case_acronyms)]
#![allow(clippy::needless_update)]
use crate::vm::{emit, VM};

pub const X0: u8 = 0;
pub const X1: u8 = 1;
pub const X2: u8 = 2;
pub const X3: u8 = 3;
pub const X4: u8 = 4;
pub const X5: u8 = 5;
pub const X6: u8 = 6;
pub const X7: u8 = 7;
pub const LR: u8 = 30;
pub const SP_XZR: u8 = 31; // SP or XZR, depending on context

#[derive(PartialEq, Eq, Copy, Clone, Debug)]
pub enum OperandSize {
    S64 = 64,
}

#[derive(Copy, Clone, PartialEq, Eq)]
#[repr(u8)]
pub enum ShiftType {
    LSL = 0, // logical shift left
             // LSR = 1, // logical shift right
             // ASR = 2, // arithmetic shift right
             // ROR = 3, // rotate right
}

#[derive(Copy, Clone, PartialEq, Eq)]
#[repr(u8)]
#[allow(dead_code)]
pub enum Condition {
    EQ = 0,  // equal
    NE = 1,  // not equal
    CS = 2,  // carry set, also HS (unsigned >=)
    CC = 3,  // carry clear, also LO (unsigned <)
    HI = 8,  // unsigned >
    LS = 9,  // unsigned <=
    GE = 10, // signed >=
    LT = 11, // signed <
    GT = 12, // signed >
    LE = 13, // signed <=
             // AL = 14, // always
}
#[allow(dead_code)]
impl Condition {
    // Aliases
    pub const HS: Condition = Condition::CS; // unsigned >=
    pub const LO: Condition = Condition::CC; // unsigned <
}

#[derive(PartialEq, Eq, Copy, Clone)]
pub enum ARM64MemoryOperand {
    OffsetPreIndex(i16),
    OffsetPostIndex(i16),
    OffsetIndex(u8),
}

// Instructions are grouped based on the encoding scheme used
#[derive(PartialEq, Eq, Copy, Clone)]
pub enum ARM64Instruction {
    LogicalRegister(ARM64InstructionLogicalShiftedRegister),
    AddSubRegister(ARM64InstructionLogicalShiftedRegister),
    ConditionalBranch(ARM64InstructionConditonalBranch),
    MovWideImm(ARM64InstructionWideImm),
    DataProcessing2Src(ARM64InstructionDataProcessing),
    Load(ARM64InstructionLoadStore),
    Store(ARM64InstructionLoadStore),
    RET,
}

#[derive(PartialEq, Eq, Copy, Clone)]
pub struct ARM64InstructionLogicalShiftedRegister {
    pub size: OperandSize,
    pub opcode: u8,            // 2 bits
    pub n: u8,                 // negation (1 bit)
    pub shift_type: ShiftType, // 2 bits
    pub dest: u8,              // Rd, 5 bits
    pub src1: u8,              // Rn, 5 bits
    pub src2: u8,              // Rm, 5 bits
    pub imm6: u8,              // shift amount (0-31 or 0-63)
}

impl Default for ARM64InstructionLogicalShiftedRegister {
    fn default() -> Self {
        Self {
            size: OperandSize::S64,
            opcode: 0,
            n: 0,
            shift_type: ShiftType::LSL,
            dest: 0,
            src1: 0,
            src2: 0,
            imm6: 0,
        }
    }
}

#[derive(PartialEq, Eq, Copy, Clone)]
pub struct ARM64InstructionDataProcessing {
    pub size: OperandSize,
    pub opcode: u8, // 6 bits
    pub dest: u8,   // Rd, 5 bits
    pub src1: u8,   // Rn, 5 bits
    pub src2: u8,   // Rm, 5 bits, only used in 2, 3-src insts
    pub src3: u8,   // R1, 5 bits, only used in 3-src insts
    pub o0: u8,     // 1 bit, used only in 3-src insts
}

impl Default for ARM64InstructionDataProcessing {
    fn default() -> Self {
        Self {
            size: OperandSize::S64,
            opcode: 0,
            dest: 0,
            src1: 0,
            src2: 0,
            src3: 0,
            o0: 0,
        }
    }
}

#[derive(PartialEq, Eq, Copy, Clone)]
pub struct ARM64InstructionWideImm {
    pub size: OperandSize,
    pub opcode: u8, // 2 bits
    pub hw: u8,     // shift (0, 16, 32, 48), encoded as 2-bits
    pub dest: u8,   // Rd, 5 bits
    pub imm16: u16, // imm6
}

#[derive(PartialEq, Eq, Copy, Clone)]
pub struct ARM64InstructionConditonalBranch {
    pub cond: u8,   // 4 bits
    pub imm19: i32, // offset from current instruction, divided by 4
}

// Load

#[derive(PartialEq, Eq, Copy, Clone)]
pub struct ARM64InstructionLoadStore {
    pub size: OperandSize,
    pub data: u8, // Rt, 5 bits
    pub base: u8, // Rn, 5 bits (base register)
    pub mem: ARM64MemoryOperand,
}

impl ARM64Instruction {
    pub fn emit(&self, vm: &mut VM) {
        let mut ins: u32 = 0;

        match self {
            ARM64Instruction::LogicalRegister(s) | ARM64Instruction::AddSubRegister(s) => {
                ins |= (s.dest & 0b11111) as u32;
                ins |= ((s.src1 & 0b11111) as u32) << 5;
                ins |= ((s.src2 & 0b11111) as u32) << 16;
                ins |= ((s.imm6 & 0b111111) as u32) << 10;
                ins |= ((s.n & 0b1) as u32) << 21;
                ins |= (s.shift_type as u32) << 22;
                ins |= ((s.opcode & 0b11) as u32) << 29;

                match self {
                    ARM64Instruction::LogicalRegister(_) => ins |= 0b01010u32 << 24,
                    ARM64Instruction::AddSubRegister(_) => ins |= 0b01011u32 << 24,
                    _ => unreachable!(),
                };

                let sf: u8 = match s.size {
                    OperandSize::S64 => 1,
                };

                ins |= (sf as u32) << 31;
            }
            ARM64Instruction::DataProcessing2Src(s) => {
                ins |= (s.dest & 0b11111) as u32;
                ins |= ((s.src1 & 0b11111) as u32) << 5;
                ins |= ((s.src2 & 0b11111) as u32) << 16;
                ins |= ((s.opcode & 0b111111) as u32) << 10;
                ins |= 0b11010110u32 << 21;
                let sf: u8 = match s.size {
                    OperandSize::S64 => 1,
                };

                ins |= (sf as u32) << 31;
            }
            ARM64Instruction::MovWideImm(s) => {
                ins |= (s.dest & 0b11111) as u32;
                ins |= (s.imm16 as u32) << 5;
                ins |= ((s.hw & 0b11) as u32) << 21;
                ins |= ((s.opcode & 0b11) as u32) << 29;

                match self {
                    ARM64Instruction::MovWideImm(_) => ins |= 0b100101u32 << 23,
                    _ => unreachable!(),
                };

                let sf: u8 = match s.size {
                    OperandSize::S64 => 1,
                };

                ins |= (sf as u32) << 31;
            }
            ARM64Instruction::ConditionalBranch(s) => {
                ins |= (s.cond & 0b1111) as u32;
                ins |= ((s.imm19 as u32) & ((1u32 << 19) - 1u32)) << 5;
                ins |= 0b01010100u32 << 24;
            }
            ARM64Instruction::RET => {
                ins = 0xd65f03c0;
            }
            ARM64Instruction::Load(s) | ARM64Instruction::Store(s) => {
                ins |= (s.data & 0b11111) as u32;
                ins |= ((s.base & 0b11111) as u32) << 5;
                let mode = match s.mem {
                    ARM64MemoryOperand::OffsetPreIndex(_) => 0b11,
                    ARM64MemoryOperand::OffsetPostIndex(_) => 0b01,
                    ARM64MemoryOperand::OffsetIndex(_) => 0b10,
                };
                ins |= (mode as u32) << 10;

                // Encode the memory operand
                match s.mem {
                    ARM64MemoryOperand::OffsetPreIndex(imm9)
                    | ARM64MemoryOperand::OffsetPostIndex(imm9) => {
                        ins |= ((imm9 & 0b111111111) as u32) << 12;
                    }
                    ARM64MemoryOperand::OffsetIndex(idx_reg) => {
                        ins |= 0b0111u32 << 12;
                        ins |= ((idx_reg & 0b11111) as u32) << 16;
                    }
                };

                // Opcode (we choose the zero-extending version for all)
                match s.mem {
                    ARM64MemoryOperand::OffsetPreIndex(_)
                    | ARM64MemoryOperand::OffsetPostIndex(_) => {
                        ins |= (if matches!(self, ARM64Instruction::Load(_)) {
                            0b111000010u32
                        } else {
                            0b111000000
                        }) << 21;
                    }
                    ARM64MemoryOperand::OffsetIndex(_) => {
                        ins |= (if matches!(self, ARM64Instruction::Load(_)) {
                            0b111000011u32
                        } else {
                            0b111000001
                        }) << 21;
                    }
                };

                // Encode size
                let size: u32 = match s.size {
                    OperandSize::S64 => 0b11,
                };
                ins |= size << 30;
            }
        }

        emit::<u32>(vm, ins);
    }

    /// Move source to destination
    #[must_use]
    pub fn mov(size: OperandSize, source: u8, destination: u8) -> Self {
        // mov is same as ORR <dst>, XZR, <src>
        Self::LogicalRegister(ARM64InstructionLogicalShiftedRegister {
            size,
            opcode: 1,
            n: 0,
            dest: destination,
            src1: SP_XZR,
            src2: source,
            ..ARM64InstructionLogicalShiftedRegister::default()
        })
    }

    #[must_use]
    pub fn eor(size: OperandSize, source: u8, destination: u8) -> Self {
        Self::LogicalRegister(ARM64InstructionLogicalShiftedRegister {
            size,
            opcode: 2,
            n: 0,
            dest: destination,
            src1: destination,
            src2: source,
            ..ARM64InstructionLogicalShiftedRegister::default()
        })
    }

    #[must_use]
    pub fn add(size: OperandSize, src1: u8, src2: u8, destination: u8) -> Self {
        Self::AddSubRegister(ARM64InstructionLogicalShiftedRegister {
            size,
            opcode: 0,
            n: 0,
            dest: destination,
            src1,
            src2,
            ..ARM64InstructionLogicalShiftedRegister::default()
        })
    }

    // destination -= source
    #[must_use]
    pub fn sub(size: OperandSize, src1: u8, src2: u8, destination: u8) -> Self {
        Self::AddSubRegister(ARM64InstructionLogicalShiftedRegister {
            size,
            opcode: 2,
            n: 0,
            dest: destination,
            src1,
            src2,
            ..ARM64InstructionLogicalShiftedRegister::default()
        })
    }

    // destination <=> source
    #[must_use]
    pub fn cmp(size: OperandSize, source: u8, destination: u8) -> Self {
        Self::AddSubRegister(ARM64InstructionLogicalShiftedRegister {
            size,
            opcode: 3,
            n: 0,
            dest: SP_XZR,
            src1: destination,
            src2: source,
            ..ARM64InstructionLogicalShiftedRegister::default()
        })
    }

    #[must_use]
    pub fn lsl_reg(size: OperandSize, src: u8, shift: u8, destination: u8) -> Self {
        Self::DataProcessing2Src(ARM64InstructionDataProcessing {
            size,
            opcode: 0b001000,
            dest: destination,
            src1: src,
            src2: shift,
            ..ARM64InstructionDataProcessing::default()
        })
    }

    #[must_use]
    pub fn lsr_reg(size: OperandSize, src: u8, shift: u8, destination: u8) -> Self {
        Self::DataProcessing2Src(ARM64InstructionDataProcessing {
            size,
            opcode: 0b001001,
            dest: destination,
            src1: src,
            src2: shift,
            ..ARM64InstructionDataProcessing::default()
        })
    }

    // conditional branch
    #[must_use]
    pub fn b_cond(cond: Condition, imm19: i32) -> Self {
        Self::ConditionalBranch(ARM64InstructionConditonalBranch {
            cond: cond as u8,
            imm19,
        })
    }

    #[must_use]
    pub fn ret() -> Self {
        Self::RET
    }

    // movk (64-bit)
    #[must_use]
    pub fn movk(destination: u8, shift_16: u8, immediate: u16) -> Self {
        debug_assert!((0..4).contains(&shift_16));
        Self::MovWideImm(ARM64InstructionWideImm {
            size: OperandSize::S64,
            dest: destination,
            hw: shift_16,
            imm16: immediate,
            opcode: 3,
        })
    }

    // mvn (bitwise NOT)
    #[must_use]
    pub fn mvn(size: OperandSize, source: u8, destination: u8) -> Self {
        Self::LogicalRegister(ARM64InstructionLogicalShiftedRegister {
            size,
            opcode: 1,
            n: 1,
            dest: destination,
            src1: SP_XZR,
            src2: source,
            ..ARM64InstructionLogicalShiftedRegister::default()
        })
    }

    /// Load data from [source + offset]
    #[must_use]
    pub fn load(size: OperandSize, source: u8, indirect: ARM64MemoryOperand, data: u8) -> Self {
        match indirect {
            ARM64MemoryOperand::OffsetPreIndex(_) | ARM64MemoryOperand::OffsetPostIndex(_) => {
                // in arm64, loads with writeback to the base register cannot also use this
                // register as the dest
                debug_assert_ne!(source, data);
            }
            _ => {}
        }
        Self::Load(ARM64InstructionLoadStore {
            size,
            data,
            base: source,
            mem: indirect,
        })
    }

    #[must_use]
    pub fn store(size: OperandSize, data: u8, source: u8, indirect: ARM64MemoryOperand) -> Self {
        match indirect {
            ARM64MemoryOperand::OffsetPreIndex(_) | ARM64MemoryOperand::OffsetPostIndex(_) => {
                // in arm64, loads with writeback to the base register cannot also use this
                // register as the dest
                debug_assert_ne!(source, data);
            }
            _ => {}
        }
        Self::Store(ARM64InstructionLoadStore {
            size,
            data,
            base: source,
            mem: indirect,
        })
    }
}
