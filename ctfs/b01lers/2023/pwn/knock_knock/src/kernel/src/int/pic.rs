use crate::arch::x64::*;

pub(super) const PICM_COMMAND: u16 = 0x20;
const PICM_DATA: u16 = 0x21;

pub(super) const PICS_COMMAND: u16 = 0xa0;
const PICS_DATA: u16 = 0xa1;

pub(super) const PIC_EOI: u8 = 0x20;

const ICW1_ICW4: u8 = 0x01;
const ICW1_SINGLE: u8 = 0x02;
const ICW1_INTERVAL4: u8 = 0x04;
const ICW1_LEVEL: u8 = 0x08;
const ICW1_INIT: u8 = 0x10;

const ICW4_8086: u8 = 0x01;
const ICW4_AUTO: u8 = 0x02;
const ICW4_BUF_SLAVE: u8 = 0x08;
const ICW4_BUF_MASTER: u8 = 0x0c;
const ICW4_SFNM: u8 = 0x10;

pub const PICM_OFFSET: u8 = 32;
pub const PICS_OFFSET: u8 = 40;

const PICM_DISABLE_OFFSET: u8 = 0xf8;
const PICS_DISABLE_OFFSET: u8 = 0xf8;

pub fn remap(moffset: u8, soffset: u8) {
    let s1 = inb(PICM_DATA);
    let s2 = inb(PICS_DATA);

    outb(PICM_COMMAND, ICW1_INIT | ICW1_ICW4);
    outb(PICS_COMMAND, ICW1_INIT | ICW1_ICW4);

    outb(PICM_DATA, moffset);
    outb(PICS_DATA, soffset);

    outb(PICM_DATA, 0b100);
    outb(PICS_DATA, 0b10);

    outb(PICM_DATA, ICW4_8086);
    outb(PICS_DATA, ICW4_8086);

    outb(PICM_DATA, s1);
    outb(PICS_DATA, s2);
}

pub fn eoi(secondary_pic: bool) {
    if secondary_pic {
        outb(PICS_COMMAND, PIC_EOI);
    }
    
    outb(PICM_COMMAND, PIC_EOI);
}

pub fn disable() {
    remap(PICM_DISABLE_OFFSET, PICS_DISABLE_OFFSET);
    outb(PICM_DATA, 0xff);
    outb(PICS_DATA, 0xff);
}
