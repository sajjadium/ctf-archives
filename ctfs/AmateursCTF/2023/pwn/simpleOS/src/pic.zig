const pio = @import("pio.zig");

const PRIMARY_PIC = 0x20;
const SECONDARY_PIC = 0xA0;
const PRIMARY_PIC_CMD = PRIMARY_PIC;
const PRIMARY_PIC_DATA = PRIMARY_PIC + 1;
const SECONDARY_PIC_CMD = SECONDARY_PIC;
const SECONDARY_PIC_DATA = SECONDARY_PIC + 1;

const PIC_EOI = 0x20; // PIC end of interrupt
const PIC_READ_IRR = 0x0A;
const PIC_READ_ISR = 0x0B;

const ICW1_ICW4 = 0x01;
const ICW1_SINGLE = 0x02;
const ICW_INTERVAL4 = 0x04;
const ICW1_LEVEL = 0x08;
const ICW1_INIT = 0x10;

const ICW4_8086 = 0x01;
const ICW4_AUTO = 0x02;
const ICW4_BUF_SECONDARY = 0x08;
const ICW4_BUF_PRIMARY = 0x0C;
const ICW4_SFNM = 0x10;

pub const PRIMARY_PIC_VECTOR = 0x20;
pub const SECONDARY_PIC_VECTOR = 0x28;

// initializes primary and secondary PIC
// remaps primary interrupt vector to int 0x20..0x28
// remaps secondary interrupt vector to int 0x28..0x30
pub fn init() void {
    //const mask1 = pio.in8(PRIMARY_PIC_DATA);
    //const mask2 = pio.in8(SECONDARY_PIC_DATA);

    pio.out8(PRIMARY_PIC_CMD, ICW1_INIT | ICW1_ICW4); // starts the initialization sequence (in cascade mode)
    pio.wait();
    pio.out8(SECONDARY_PIC_CMD, ICW1_INIT | ICW1_ICW4);
    pio.wait();
    pio.out8(PRIMARY_PIC_DATA, PRIMARY_PIC_VECTOR); // ICW2: primary PIC vector offset
    pio.wait();
    pio.out8(SECONDARY_PIC_DATA, SECONDARY_PIC_VECTOR); // ICW2: secondary PIC vector offset
    pio.wait();
    pio.out8(PRIMARY_PIC_DATA, 4); // ICW3: tell primary PIC that there is a secondary PIC at IRQ2 (0000 0100)
    pio.wait();
    pio.out8(SECONDARY_PIC_DATA, 2); // ICW3: tell secondary PIC its cascade identity (0000 0010)
    pio.wait();

    pio.out8(PRIMARY_PIC_DATA, ICW4_8086);
    pio.wait();
    pio.out8(SECONDARY_PIC_DATA, ICW4_8086);
    pio.wait();

    // shutoff timer interrupt
    pio.out8(PRIMARY_PIC_DATA, 0x01);
    pio.out8(SECONDARY_PIC_DATA, 0x00);
}

pub fn eoi(irq: usize) void {
    if (irq - PRIMARY_PIC_VECTOR >= 8) {
        pio.out8(SECONDARY_PIC_CMD, PIC_EOI);
    }
    pio.out8(PRIMARY_PIC_CMD, PIC_EOI);
}
