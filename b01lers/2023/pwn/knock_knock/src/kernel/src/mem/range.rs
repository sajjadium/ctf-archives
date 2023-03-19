use core::alloc::Layout;
use core::cmp::min;
use core::marker::PhantomData;
use core::slice;

use super::{Allocation, PhysAddr, VirtAddr};
use crate::prelude::*;

pub const MAX_VIRT_ADDR: usize = 1 << 47;

pub fn align_down_to_page_size(n: usize) -> usize {
    if n >= PageSize::G1 as usize {
        PageSize::G1 as usize
    } else if n >= PageSize::M2 as usize {
        PageSize::M2 as usize
    } else if n >= PageSize::K4 as usize {
        PageSize::K4 as usize
    } else {
        0
    }
}

#[repr(u64)]
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum PageSize {
    K4 = 0x1000,
    M2 = 0x200000,
    G1 = 0x40000000,
}

impl PageSize {
    pub fn from_u64(n: u64) -> Self {
        Self::from_usize(n as _)
    }

    pub fn from_usize(n: usize) -> Self {
        Self::try_from_usize(n)
            .expect("tried to convert integer to PageSize, but it wasn't a valid page size")
    }

    pub fn try_from_usize(n: usize) -> Option<Self> {
        match n {
            0x1000 => Some(Self::K4),
            0x200000 => Some(Self::M2),
            0x40000000 => Some(Self::G1),
            _ => None,
        }
    }
}

macro_rules! impl_addr_range {
    (
        $addr:ident,
        $frame:ident,
        $range_trait:ident,
        $aligned_range:ident,
        $unaligned_range:ident,
        $iter:ident
    ) => {
        #[derive(Debug, Clone, Copy)]
        pub enum $frame {
            K4($addr),
            M2($addr),
            G1($addr),
        }

        impl $frame {
            pub fn new(addr: $addr, size: PageSize) -> Self {
                match size {
                    PageSize::K4 => Self::K4(addr.align_down(size as usize)),
                    PageSize::M2 => Self::M2(addr.align_down(size as usize)),
                    PageSize::G1 => Self::G1(addr.align_down(size as usize)),
                }
            }

            pub fn start_addr(&self) -> $addr {
                match self {
                    Self::K4(addr) => *addr,
                    Self::M2(addr) => *addr,
                    Self::G1(addr) => *addr,
                }
            }

            pub fn end_addr(&self) -> $addr {
                match self {
                    Self::K4(addr) => *addr + PageSize::K4 as usize,
                    Self::M2(addr) => *addr + PageSize::M2 as usize,
                    Self::G1(addr) => *addr + PageSize::G1 as usize,
                }
            }

            pub fn get_size(&self) -> PageSize {
                match self {
                    Self::K4(_) => PageSize::K4,
                    Self::M2(_) => PageSize::M2,
                    Self::G1(_) => PageSize::G1,
                }
            }
        }

        pub trait $range_trait {
            fn addr(&self) -> $addr;
            fn size(&self) -> usize;

            fn addr_mut(&mut self) -> &mut $addr;
            fn size_mut(&mut self) -> &mut usize;

            fn is_aligned(&self) -> bool;
            fn as_unaligned(&self) -> $unaligned_range;
            fn as_inside_aligned(&self) -> Option<$aligned_range>;
            fn as_aligned(&self) -> $aligned_range;
            fn try_as_aligned(&self) -> Option<$aligned_range>;

            fn as_usize(&self) -> usize {
                self.addr().as_usize()
            }

            fn end_addr(&self) -> $addr {
                self.addr() + self.size()
            }

            fn end_usize(&self) -> usize {
                self.as_usize() + self.size()
            }

            unsafe fn as_slice(&self) -> &[u8] {
                unsafe { slice::from_raw_parts(self.as_usize() as *const u8, self.size()) }
            }

            unsafe fn as_slice_mut(&self) -> &mut [u8] {
                unsafe { slice::from_raw_parts_mut(self.as_usize() as *mut u8, self.size()) }
            }

            fn contains(&self, addr: $addr) -> bool {
                (addr >= self.addr()) && (addr < (self.addr() + self.size()))
            }

            fn contains_range(&self, range: &dyn $range_trait) -> bool {
                self.contains(range.addr()) || self.contains(range.addr() + range.size())
            }

            fn full_contains_range(&self, range: &dyn $range_trait) -> bool {
                if range.size() == 0 {
                    self.contains(range.addr())
                } else {
                    self.contains(range.addr()) && self.contains(range.addr() + range.size() - 1)
                }
            }

            fn is_power2_size_align(&self) -> bool {
                self.size().is_power_of_two() && align_of(self.as_usize()) >= self.size()
            }

            fn merge(&self, other: Self) -> Option<Self>
            where
                Self: Sized;

            fn split_at(&self, range: Self) -> (Option<Self>, Option<Self>)
            where
                Self: Sized;
            
            fn split_at_iter(&self, range: Self) -> impl Iterator<Item = Self>
            where Self: Sized {
                let (first_out, second_out) = self.split_at(range);
                first_out.into_iter()
                    .chain(second_out)
            }

            fn get_take_size(&self) -> Option<PageSize> {
                PageSize::try_from_usize(min(
                    align_down_to_page_size(self.size()),
                    align_down_to_page_size(align_of(self.addr().as_usize())),
                ))
            }

            fn take(&mut self, size: PageSize) -> Option<$frame> {
                let take_size = self.get_take_size()?;
                if size > take_size {
                    None
                } else {
                    let size = size as usize;
                    let addr = self.addr();
                    *self.addr_mut() += size;
                    *self.size_mut() -= size;
                    Some($frame::new(addr, PageSize::from_usize(size)))
                }
            }

            fn iter(&self) -> $iter {
                $iter {
                    start: self.addr(),
                    end: self.end_addr(),
                    life: PhantomData,
                }
            }
        }

        #[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
        pub struct $unaligned_range {
            addr: $addr,
            size: usize,
        }

        impl $unaligned_range {
            pub fn new(addr: $addr, size: usize) -> Self {
                Self {
                    addr,
                    size,
                }
            }

            pub fn new_aligned_inside(addr: $addr, size: usize) -> Option<Self> {
                let start_addr = addr.align_up(PAGE_SIZE);
                let end_addr = (addr + size).align_down(PAGE_SIZE);
                if start_addr > end_addr {
                    None
                } else {
                    Some(Self {
                        addr: start_addr,
                        size: end_addr - start_addr,
                    })
                }
            }

            pub fn new_aligned(addr: $addr, size: usize) -> Self {
                let addr2 = (addr + size).align_up(PAGE_SIZE);
                Self {
                    addr: addr.align_down(PAGE_SIZE),
                    size: align_up((addr2 - addr), PAGE_SIZE),
                }
            }

            pub fn try_new_aligned(addr: $addr, size: usize) -> Option<Self> {
                if align_of(addr.as_usize()) < PAGE_SIZE || align_of(size) < PAGE_SIZE {
                    None
                } else {
                    Some(Self {
                        addr,
                        size,
                    })
                }
            }

            pub fn null() -> Self {
                Self {
                    addr: $addr::new(0),
                    size: 0,
                }
            }

            pub fn take_layout(&mut self, layout: Layout) -> Option<Self> {
                let start_addr = self.addr().align_up(layout.align());
                let new_addr = start_addr + layout.size();

                if new_addr > self.end_addr() {
                    None
                } else {
                    let size = new_addr - start_addr;
                    self.addr = new_addr;
                    self.size -= size;
                    Some(Self::new(start_addr, size))
                }
            }
        }

        impl $range_trait for $unaligned_range {
            fn addr(&self) -> $addr {
                self.addr
            }

            fn size(&self) -> usize {
                self.size
            }

            fn addr_mut(&mut self) -> &mut $addr {
                &mut self.addr
            }

            fn size_mut(&mut self) -> &mut usize {
                &mut self.size
            }

            fn is_aligned(&self) -> bool {
                align_of(self.as_usize()) >= PAGE_SIZE && align_of(self.end_usize()) >= PAGE_SIZE
            }

            fn as_unaligned(&self) -> $unaligned_range {
                *self
            }

            fn as_inside_aligned(&self) -> Option<$aligned_range> {
                $aligned_range::new_aligned_inside(self.addr, self.size)
            }

            fn as_aligned(&self) -> $aligned_range {
                $aligned_range::new_aligned(self.addr, self.size)
            }

            fn try_as_aligned(&self) -> Option<$aligned_range> {
                $aligned_range::try_new_aligned(self.addr, self.size)
            }

            fn merge(&self, other: Self) -> Option<Self>
            where
                Self: Sized,
            {
                if self.end_addr() == other.addr() {
                    Some(Self::new(self.addr(), self.size() + other.size()))
                } else if other.end_addr() == self.addr() {
                    Some(Self::new(other.addr(), self.size() + other.size()))
                } else {
                    None
                }
            }

            fn split_at(&self, range: Self) -> (Option<Self>, Option<Self>)
            where
                Self: Sized,
            {
                let sbegin = self.addr();
                let send = self.addr() + self.size();

                let begin = range.addr();
                let end = begin + range.size();

                if !self.contains_range(&range) {
                    (Some(*self), None)
                } else if begin <= sbegin && end >= send {
                    (None, None)
                } else if self.contains(begin - 1usize) && !self.contains(end + 1usize) {
                    (Some(Self::new(sbegin, begin - sbegin)), None)
                } else if self.contains(end + 1usize) && !self.contains(begin - 1usize) {
                    (Some(Self::new(end, send - end)), None)
                } else {
                    (
                        Some(Self::new(sbegin, (begin - sbegin) as usize)),
                        Some(Self::new(end, send - end)),
                    )
                }
            }
        }

        impl From<&$aligned_range> for $unaligned_range {
            fn from(range: &$aligned_range) -> Self {
                Self {
                    addr: range.addr,
                    size: range.size,
                }
            }
        }

        #[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
        pub struct $aligned_range {
            addr: $addr,
            size: usize,
        }

        impl $aligned_range {
            pub fn new(addr: $addr, size: usize) -> Self {
                Self::try_new_aligned(addr, size)
                    .expect("invalid address and size passed to AlignedRange::new()")
            }

            pub fn new_aligned_inside(addr: $addr, size: usize) -> Option<Self> {
                let start_addr = addr.align_up(PAGE_SIZE);
                let end_addr = (addr + size).align_down(PAGE_SIZE);
                if start_addr > end_addr {
                    None
                } else {
                    Some(Self {
                        addr: start_addr,
                        size: end_addr - start_addr,
                    })
                }
            }

            pub fn new_aligned(addr: $addr, size: usize) -> Self {
                let addr2 = (addr + size).align_up(PAGE_SIZE);
                Self {
                    addr: addr.align_down(PAGE_SIZE),
                    size: align_up((addr2 - addr), PAGE_SIZE),
                }
            }

            pub fn try_new_aligned(addr: $addr, size: usize) -> Option<Self> {
                if align_of(addr.as_usize()) < PAGE_SIZE || align_of(size) < PAGE_SIZE {
                    None
                } else {
                    Some(Self {
                        addr,
                        size,
                    })
                }
            }

            pub fn page_size(&self) -> usize {
                self.size / PAGE_SIZE
            }

            pub fn null() -> Self {
                Self {
                    addr: $addr::new(0),
                    size: 0,
                }
            }
        }

        impl $range_trait for $aligned_range {
            fn addr(&self) -> $addr {
                self.addr
            }

            fn size(&self) -> usize {
                self.size
            }

            fn addr_mut(&mut self) -> &mut $addr {
                &mut self.addr
            }

            fn size_mut(&mut self) -> &mut usize {
                &mut self.size
            }

            fn is_aligned(&self) -> bool {
                true
            }

            fn as_unaligned(&self) -> $unaligned_range {
                self.into()
            }

            fn as_inside_aligned(&self) -> Option<$aligned_range> {
                Some(*self)
            }

            fn as_aligned(&self) -> $aligned_range {
                *self
            }

            fn try_as_aligned(&self) -> Option<$aligned_range> {
                Some(*self)
            }

            fn merge(&self, other: Self) -> Option<Self>
            where
                Self: Sized,
            {
                if self.end_addr() == other.addr() {
                    Some(Self::new_aligned(self.addr(), self.size() + other.size()))
                } else if other.end_addr() == self.addr() {
                    Some(Self::new_aligned(other.addr(), self.size() + other.size()))
                } else {
                    None
                }
            }

            fn split_at(&self, range: Self) -> (Option<Self>, Option<Self>)
            where
                Self: Sized,
            {
                let sbegin = self.addr();
                let send = self.addr() + self.size();

                let begin = range.addr();
                let end = begin + range.size();

                if !self.contains_range(&range) {
                    (Some(*self), None)
                } else if begin <= sbegin && end >= send {
                    (None, None)
                } else if self.contains(begin - 1usize) && !self.contains(end + 1usize) {
                    (Some(Self::new_aligned(sbegin, begin - sbegin)), None)
                } else if self.contains(end + 1usize) && !self.contains(begin - 1usize) {
                    (Some(Self::new_aligned(end, send - end)), None)
                } else {
                    (
                        Some(Self::new_aligned(sbegin, (begin - sbegin) as usize)),
                        Some(Self::new_aligned(end, send - end)),
                    )
                }
            }
        }

        #[derive(Debug, Clone, Copy)]
        pub struct $iter<'a> {
            start: $addr,
            end: $addr,
            life: PhantomData<&'a dyn $range_trait>,
        }

        impl Iterator for $iter<'_> {
            type Item = $frame;

            fn next(&mut self) -> Option<Self::Item> {
                if self.start >= self.end {
                    return None;
                }

                let size = min(
                    align_of(self.start.as_usize()),
                    1 << log2(self.end - self.start),
                );
                let size = align_down_to_page_size(size);
                self.start += size;
                let size = PageSize::from_usize(size);
                Some($frame::new(self.start, size))
            }
        }
    };
}

impl_addr_range! {PhysAddr, PhysFrame, PhysRangeInner, APhysRange, UPhysRange, PhysRangeIter}
impl_addr_range! {VirtAddr, VirtFrame, VirtRangeInner, AVirtRange, UVirtRange, VirtRangeIter}

pub trait PhysRange: PhysRangeInner {
    fn to_virt(&self) -> UVirtRange {
        let _tmp = self.end_addr().to_virt();
        let addr = self.addr().to_virt();
        UVirtRange::new(addr, self.size())
    }
}

impl<T: PhysRangeInner> PhysRange for T {}

pub trait VirtRange: VirtRangeInner {
    fn to_phys(&self) -> UPhysRange {
        let _tmp = self.end_addr().to_phys();
        let addr = self.addr().to_phys();
        UPhysRange::new(addr, self.size())
    }
}

impl<T: VirtRangeInner> VirtRange for T {}

impl From<Allocation> for UPhysRange {
    fn from(mem: Allocation) -> Self {
        Self::new(mem.addr().to_phys(), mem.size())
    }
}
