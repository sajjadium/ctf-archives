pub type KResult<T> = Result<T, SysErr>;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
#[repr(usize)]
pub enum SysErr {
    Ok = 0,
    OutOfMem = 3,
    InvlMemZone = 9,
    InvlVirtAddr = 10,
    InvlAlign = 11,
    InvlSyscall = 13,
    Unknown = 14,
}

impl SysErr {
    pub fn new(n: usize) -> Option<Self> {
        if n > Self::Unknown as usize {
            None
        } else {
            unsafe { Some(core::mem::transmute(n)) }
        }
    }

    pub const fn num(&self) -> usize {
        *self as usize
    }

    pub const fn as_str(&self) -> &'static str {
        match self {
            Self::Ok => "no error",
            Self::OutOfMem => "out of memory",
            Self::InvlMemZone => "invalid memory zone or memory zone collision",
            Self::InvlVirtAddr => "non canonical address",
            Self::InvlAlign => "invalid alignment",
            Self::InvlSyscall => "invalid syscall number",
            Self::Unknown => "unknown error",
        }
    }
}