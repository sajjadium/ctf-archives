const std = @import("std");
const term = @import("term.zig");
const arch = @import("arch.zig");
const pic = @import("pic.zig");
const pio = @import("pio.zig");

pub const IDT_INTERRUPT = 0b1110;
pub const IDT_TRAP = 0b1111;

pub const Descriptor = packed struct {
    offset_lo: u16,
    gdt_segment: u16,
    interrupt_stack_table_offset: u8,
    flags: u8,
    offset_hi: u42,
    reserved: u32,
};

pub const InterruptTableDescriptor = packed struct {
    size: u16,
    offset: usize,
};

var interrupt_table: [256]Descriptor = undefined;
var interrupt_table_descriptor: InterruptTableDescriptor = undefined;

pub fn set(n: usize, handler: *const fn () callconv(.C) void, gate_type: u8, privilege: u8, present: u8) void {
    const offset = @ptrToInt(handler);
    const lo = @intCast(u16, offset & 0xFFFF);
    const hi = @intCast(u42, offset >> 16);
    const flags = (present << 7) | (privilege << 5) | gate_type;

    interrupt_table[n] = Descriptor{
        .offset_lo = lo,
        .gdt_segment = 0x08,
        .interrupt_stack_table_offset = 0x00,
        .flags = flags,
        .offset_hi = hi,
        .reserved = 0,
    };
}

extern fn interrupt0() void;
extern fn interrupt1() void;
extern fn interrupt2() void;
extern fn interrupt3() void;
extern fn interrupt4() void;
extern fn interrupt5() void;
extern fn interrupt6() void;
extern fn interrupt7() void;
extern fn interrupt8() void;
extern fn interrupt9() void;
extern fn interrupt10() void;
extern fn interrupt11() void;
extern fn interrupt12() void;
extern fn interrupt13() void;
extern fn interrupt14() void;
extern fn interrupt15() void;
extern fn interrupt16() void;
extern fn interrupt17() void;
extern fn interrupt18() void;
extern fn interrupt19() void;
extern fn interrupt20() void;
extern fn interrupt21() void;
extern fn interrupt22() void;
extern fn interrupt23() void;
extern fn interrupt24() void;
extern fn interrupt25() void;
extern fn interrupt26() void;
extern fn interrupt27() void;
extern fn interrupt28() void;
extern fn interrupt29() void;
extern fn interrupt30() void;
extern fn interrupt31() void;
extern fn interrupt32() void;
extern fn interrupt33() void;
extern fn interrupt34() void;
extern fn interrupt35() void;
extern fn interrupt36() void;
extern fn interrupt37() void;
extern fn interrupt38() void;
extern fn interrupt39() void;
extern fn interrupt40() void;
extern fn interrupt41() void;
extern fn interrupt42() void;
extern fn interrupt43() void;
extern fn interrupt44() void;
extern fn interrupt45() void;
extern fn interrupt46() void;
extern fn interrupt47() void;
extern fn interrupt48() void;
extern fn interrupt49() void;
extern fn interrupt50() void;
extern fn interrupt51() void;
extern fn interrupt52() void;
extern fn interrupt53() void;
extern fn interrupt54() void;
extern fn interrupt55() void;
extern fn interrupt56() void;
extern fn interrupt57() void;
extern fn interrupt58() void;
extern fn interrupt59() void;
extern fn interrupt60() void;
extern fn interrupt61() void;
extern fn interrupt62() void;
extern fn interrupt63() void;
extern fn interrupt64() void;
extern fn interrupt65() void;
extern fn interrupt66() void;
extern fn interrupt67() void;
extern fn interrupt68() void;
extern fn interrupt69() void;
extern fn interrupt70() void;
extern fn interrupt71() void;
extern fn interrupt72() void;
extern fn interrupt73() void;
extern fn interrupt74() void;
extern fn interrupt75() void;
extern fn interrupt76() void;
extern fn interrupt77() void;
extern fn interrupt78() void;
extern fn interrupt79() void;
extern fn interrupt80() void;
extern fn interrupt81() void;
extern fn interrupt82() void;
extern fn interrupt83() void;
extern fn interrupt84() void;
extern fn interrupt85() void;
extern fn interrupt86() void;
extern fn interrupt87() void;
extern fn interrupt88() void;
extern fn interrupt89() void;
extern fn interrupt90() void;
extern fn interrupt91() void;
extern fn interrupt92() void;
extern fn interrupt93() void;
extern fn interrupt94() void;
extern fn interrupt95() void;
extern fn interrupt96() void;
extern fn interrupt97() void;
extern fn interrupt98() void;
extern fn interrupt99() void;
extern fn interrupt100() void;
extern fn interrupt101() void;
extern fn interrupt102() void;
extern fn interrupt103() void;
extern fn interrupt104() void;
extern fn interrupt105() void;
extern fn interrupt106() void;
extern fn interrupt107() void;
extern fn interrupt108() void;
extern fn interrupt109() void;
extern fn interrupt110() void;
extern fn interrupt111() void;
extern fn interrupt112() void;
extern fn interrupt113() void;
extern fn interrupt114() void;
extern fn interrupt115() void;
extern fn interrupt116() void;
extern fn interrupt117() void;
extern fn interrupt118() void;
extern fn interrupt119() void;
extern fn interrupt120() void;
extern fn interrupt121() void;
extern fn interrupt122() void;
extern fn interrupt123() void;
extern fn interrupt124() void;
extern fn interrupt125() void;
extern fn interrupt126() void;
extern fn interrupt127() void;
extern fn interrupt128() void;
extern fn interrupt129() void;
extern fn interrupt130() void;
extern fn interrupt131() void;
extern fn interrupt132() void;
extern fn interrupt133() void;
extern fn interrupt134() void;
extern fn interrupt135() void;
extern fn interrupt136() void;
extern fn interrupt137() void;
extern fn interrupt138() void;
extern fn interrupt139() void;
extern fn interrupt140() void;
extern fn interrupt141() void;
extern fn interrupt142() void;
extern fn interrupt143() void;
extern fn interrupt144() void;
extern fn interrupt145() void;
extern fn interrupt146() void;
extern fn interrupt147() void;
extern fn interrupt148() void;
extern fn interrupt149() void;
extern fn interrupt150() void;
extern fn interrupt151() void;
extern fn interrupt152() void;
extern fn interrupt153() void;
extern fn interrupt154() void;
extern fn interrupt155() void;
extern fn interrupt156() void;
extern fn interrupt157() void;
extern fn interrupt158() void;
extern fn interrupt159() void;
extern fn interrupt160() void;
extern fn interrupt161() void;
extern fn interrupt162() void;
extern fn interrupt163() void;
extern fn interrupt164() void;
extern fn interrupt165() void;
extern fn interrupt166() void;
extern fn interrupt167() void;
extern fn interrupt168() void;
extern fn interrupt169() void;
extern fn interrupt170() void;
extern fn interrupt171() void;
extern fn interrupt172() void;
extern fn interrupt173() void;
extern fn interrupt174() void;
extern fn interrupt175() void;
extern fn interrupt176() void;
extern fn interrupt177() void;
extern fn interrupt178() void;
extern fn interrupt179() void;
extern fn interrupt180() void;
extern fn interrupt181() void;
extern fn interrupt182() void;
extern fn interrupt183() void;
extern fn interrupt184() void;
extern fn interrupt185() void;
extern fn interrupt186() void;
extern fn interrupt187() void;
extern fn interrupt188() void;
extern fn interrupt189() void;
extern fn interrupt190() void;
extern fn interrupt191() void;
extern fn interrupt192() void;
extern fn interrupt193() void;
extern fn interrupt194() void;
extern fn interrupt195() void;
extern fn interrupt196() void;
extern fn interrupt197() void;
extern fn interrupt198() void;
extern fn interrupt199() void;
extern fn interrupt200() void;
extern fn interrupt201() void;
extern fn interrupt202() void;
extern fn interrupt203() void;
extern fn interrupt204() void;
extern fn interrupt205() void;
extern fn interrupt206() void;
extern fn interrupt207() void;
extern fn interrupt208() void;
extern fn interrupt209() void;
extern fn interrupt210() void;
extern fn interrupt211() void;
extern fn interrupt212() void;
extern fn interrupt213() void;
extern fn interrupt214() void;
extern fn interrupt215() void;
extern fn interrupt216() void;
extern fn interrupt217() void;
extern fn interrupt218() void;
extern fn interrupt219() void;
extern fn interrupt220() void;
extern fn interrupt221() void;
extern fn interrupt222() void;
extern fn interrupt223() void;
extern fn interrupt224() void;
extern fn interrupt225() void;
extern fn interrupt226() void;
extern fn interrupt227() void;
extern fn interrupt228() void;
extern fn interrupt229() void;
extern fn interrupt230() void;
extern fn interrupt231() void;
extern fn interrupt232() void;
extern fn interrupt233() void;
extern fn interrupt234() void;
extern fn interrupt235() void;
extern fn interrupt236() void;
extern fn interrupt237() void;
extern fn interrupt238() void;
extern fn interrupt239() void;
extern fn interrupt240() void;
extern fn interrupt241() void;
extern fn interrupt242() void;
extern fn interrupt243() void;
extern fn interrupt244() void;
extern fn interrupt245() void;
extern fn interrupt246() void;
extern fn interrupt247() void;
extern fn interrupt248() void;
extern fn interrupt249() void;
extern fn interrupt250() void;
extern fn interrupt251() void;
extern fn interrupt252() void;
extern fn interrupt253() void;
extern fn interrupt254() void;
extern fn interrupt255() void;

pub fn init() void {
    fill_table();
    load();
}

fn fill_table() void {
    set(0, &interrupt0, IDT_INTERRUPT, 0, 1);
    set(1, &interrupt1, IDT_INTERRUPT, 0, 1);
    set(2, &interrupt2, IDT_INTERRUPT, 0, 1);
    set(3, &interrupt3, IDT_INTERRUPT, 0, 1);
    set(4, &interrupt4, IDT_INTERRUPT, 0, 1);
    set(5, &interrupt5, IDT_INTERRUPT, 0, 1);
    set(6, &interrupt6, IDT_INTERRUPT, 0, 1);
    set(7, &interrupt7, IDT_INTERRUPT, 0, 1);
    set(8, &interrupt8, IDT_INTERRUPT, 0, 1);
    set(9, &interrupt9, IDT_INTERRUPT, 0, 1);
    set(10, &interrupt10, IDT_INTERRUPT, 0, 1);
    set(11, &interrupt11, IDT_INTERRUPT, 0, 1);
    set(12, &interrupt12, IDT_INTERRUPT, 0, 1);
    set(13, &interrupt13, IDT_INTERRUPT, 0, 1);
    set(14, &interrupt14, IDT_INTERRUPT, 0, 1);
    set(15, &interrupt15, IDT_INTERRUPT, 0, 1);
    set(16, &interrupt16, IDT_INTERRUPT, 0, 1);
    set(17, &interrupt17, IDT_INTERRUPT, 0, 1);
    set(18, &interrupt18, IDT_INTERRUPT, 0, 1);
    set(19, &interrupt19, IDT_INTERRUPT, 0, 1);
    set(20, &interrupt20, IDT_INTERRUPT, 0, 1);
    set(21, &interrupt21, IDT_INTERRUPT, 0, 1);
    set(22, &interrupt22, IDT_INTERRUPT, 0, 1);
    set(23, &interrupt23, IDT_INTERRUPT, 0, 1);
    set(24, &interrupt24, IDT_INTERRUPT, 0, 1);
    set(25, &interrupt25, IDT_INTERRUPT, 0, 1);
    set(26, &interrupt26, IDT_INTERRUPT, 0, 1);
    set(27, &interrupt27, IDT_INTERRUPT, 0, 1);
    set(28, &interrupt28, IDT_INTERRUPT, 0, 1);
    set(29, &interrupt29, IDT_INTERRUPT, 0, 1);
    set(30, &interrupt30, IDT_INTERRUPT, 0, 1);
    set(31, &interrupt31, IDT_INTERRUPT, 0, 1);
    set(32, &interrupt32, IDT_INTERRUPT, 0, 1);
    set(33, &interrupt33, IDT_INTERRUPT, 0, 1);
    set(34, &interrupt34, IDT_INTERRUPT, 0, 1);
    set(35, &interrupt35, IDT_INTERRUPT, 0, 1);
    set(36, &interrupt36, IDT_INTERRUPT, 0, 1);
    set(37, &interrupt37, IDT_INTERRUPT, 0, 1);
    set(38, &interrupt38, IDT_INTERRUPT, 0, 1);
    set(39, &interrupt39, IDT_INTERRUPT, 0, 1);
    set(40, &interrupt40, IDT_INTERRUPT, 0, 1);
    set(41, &interrupt41, IDT_INTERRUPT, 0, 1);
    set(42, &interrupt42, IDT_INTERRUPT, 0, 1);
    set(43, &interrupt43, IDT_INTERRUPT, 0, 1);
    set(44, &interrupt44, IDT_INTERRUPT, 0, 1);
    set(45, &interrupt45, IDT_INTERRUPT, 0, 1);
    set(46, &interrupt46, IDT_INTERRUPT, 0, 1);
    set(47, &interrupt47, IDT_INTERRUPT, 0, 1);
    set(48, &interrupt48, IDT_INTERRUPT, 0, 1);
    set(49, &interrupt49, IDT_INTERRUPT, 0, 1);
    set(50, &interrupt50, IDT_INTERRUPT, 0, 1);
    set(51, &interrupt51, IDT_INTERRUPT, 0, 1);
    set(52, &interrupt52, IDT_INTERRUPT, 0, 1);
    set(53, &interrupt53, IDT_INTERRUPT, 0, 1);
    set(54, &interrupt54, IDT_INTERRUPT, 0, 1);
    set(55, &interrupt55, IDT_INTERRUPT, 0, 1);
    set(56, &interrupt56, IDT_INTERRUPT, 0, 1);
    set(57, &interrupt57, IDT_INTERRUPT, 0, 1);
    set(58, &interrupt58, IDT_INTERRUPT, 0, 1);
    set(59, &interrupt59, IDT_INTERRUPT, 0, 1);
    set(60, &interrupt60, IDT_INTERRUPT, 0, 1);
    set(61, &interrupt61, IDT_INTERRUPT, 0, 1);
    set(62, &interrupt62, IDT_INTERRUPT, 0, 1);
    set(63, &interrupt63, IDT_INTERRUPT, 0, 1);
    set(64, &interrupt64, IDT_INTERRUPT, 0, 1);
    set(65, &interrupt65, IDT_INTERRUPT, 0, 1);
    set(66, &interrupt66, IDT_INTERRUPT, 0, 1);
    set(67, &interrupt67, IDT_INTERRUPT, 0, 1);
    set(68, &interrupt68, IDT_INTERRUPT, 0, 1);
    set(69, &interrupt69, IDT_INTERRUPT, 0, 1);
    set(70, &interrupt70, IDT_INTERRUPT, 0, 1);
    set(71, &interrupt71, IDT_INTERRUPT, 0, 1);
    set(72, &interrupt72, IDT_INTERRUPT, 0, 1);
    set(73, &interrupt73, IDT_INTERRUPT, 0, 1);
    set(74, &interrupt74, IDT_INTERRUPT, 0, 1);
    set(75, &interrupt75, IDT_INTERRUPT, 0, 1);
    set(76, &interrupt76, IDT_INTERRUPT, 0, 1);
    set(77, &interrupt77, IDT_INTERRUPT, 0, 1);
    set(78, &interrupt78, IDT_INTERRUPT, 0, 1);
    set(79, &interrupt79, IDT_INTERRUPT, 0, 1);
    set(80, &interrupt80, IDT_INTERRUPT, 0, 1);
    set(81, &interrupt81, IDT_INTERRUPT, 0, 1);
    set(82, &interrupt82, IDT_INTERRUPT, 0, 1);
    set(83, &interrupt83, IDT_INTERRUPT, 0, 1);
    set(84, &interrupt84, IDT_INTERRUPT, 0, 1);
    set(85, &interrupt85, IDT_INTERRUPT, 0, 1);
    set(86, &interrupt86, IDT_INTERRUPT, 0, 1);
    set(87, &interrupt87, IDT_INTERRUPT, 0, 1);
    set(88, &interrupt88, IDT_INTERRUPT, 0, 1);
    set(89, &interrupt89, IDT_INTERRUPT, 0, 1);
    set(90, &interrupt90, IDT_INTERRUPT, 0, 1);
    set(91, &interrupt91, IDT_INTERRUPT, 0, 1);
    set(92, &interrupt92, IDT_INTERRUPT, 0, 1);
    set(93, &interrupt93, IDT_INTERRUPT, 0, 1);
    set(94, &interrupt94, IDT_INTERRUPT, 0, 1);
    set(95, &interrupt95, IDT_INTERRUPT, 0, 1);
    set(96, &interrupt96, IDT_INTERRUPT, 0, 1);
    set(97, &interrupt97, IDT_INTERRUPT, 0, 1);
    set(98, &interrupt98, IDT_INTERRUPT, 0, 1);
    set(99, &interrupt99, IDT_INTERRUPT, 0, 1);
    set(100, &interrupt100, IDT_INTERRUPT, 0, 1);
    set(101, &interrupt101, IDT_INTERRUPT, 0, 1);
    set(102, &interrupt102, IDT_INTERRUPT, 0, 1);
    set(103, &interrupt103, IDT_INTERRUPT, 0, 1);
    set(104, &interrupt104, IDT_INTERRUPT, 0, 1);
    set(105, &interrupt105, IDT_INTERRUPT, 0, 1);
    set(106, &interrupt106, IDT_INTERRUPT, 0, 1);
    set(107, &interrupt107, IDT_INTERRUPT, 0, 1);
    set(108, &interrupt108, IDT_INTERRUPT, 0, 1);
    set(109, &interrupt109, IDT_INTERRUPT, 0, 1);
    set(110, &interrupt110, IDT_INTERRUPT, 0, 1);
    set(111, &interrupt111, IDT_INTERRUPT, 0, 1);
    set(112, &interrupt112, IDT_INTERRUPT, 0, 1);
    set(113, &interrupt113, IDT_INTERRUPT, 0, 1);
    set(114, &interrupt114, IDT_INTERRUPT, 0, 1);
    set(115, &interrupt115, IDT_INTERRUPT, 0, 1);
    set(116, &interrupt116, IDT_INTERRUPT, 0, 1);
    set(117, &interrupt117, IDT_INTERRUPT, 0, 1);
    set(118, &interrupt118, IDT_INTERRUPT, 0, 1);
    set(119, &interrupt119, IDT_INTERRUPT, 0, 1);
    set(120, &interrupt120, IDT_INTERRUPT, 0, 1);
    set(121, &interrupt121, IDT_INTERRUPT, 0, 1);
    set(122, &interrupt122, IDT_INTERRUPT, 0, 1);
    set(123, &interrupt123, IDT_INTERRUPT, 0, 1);
    set(124, &interrupt124, IDT_INTERRUPT, 0, 1);
    set(125, &interrupt125, IDT_INTERRUPT, 0, 1);
    set(126, &interrupt126, IDT_INTERRUPT, 0, 1);
    set(127, &interrupt127, IDT_INTERRUPT, 0, 1);
    set(128, &interrupt128, IDT_INTERRUPT, 0, 1);
    set(129, &interrupt129, IDT_INTERRUPT, 0, 1);
    set(130, &interrupt130, IDT_INTERRUPT, 0, 1);
    set(131, &interrupt131, IDT_INTERRUPT, 0, 1);
    set(132, &interrupt132, IDT_INTERRUPT, 0, 1);
    set(133, &interrupt133, IDT_INTERRUPT, 0, 1);
    set(134, &interrupt134, IDT_INTERRUPT, 0, 1);
    set(135, &interrupt135, IDT_INTERRUPT, 0, 1);
    set(136, &interrupt136, IDT_INTERRUPT, 0, 1);
    set(137, &interrupt137, IDT_INTERRUPT, 0, 1);
    set(138, &interrupt138, IDT_INTERRUPT, 0, 1);
    set(139, &interrupt139, IDT_INTERRUPT, 0, 1);
    set(140, &interrupt140, IDT_INTERRUPT, 0, 1);
    set(141, &interrupt141, IDT_INTERRUPT, 0, 1);
    set(142, &interrupt142, IDT_INTERRUPT, 0, 1);
    set(143, &interrupt143, IDT_INTERRUPT, 0, 1);
    set(144, &interrupt144, IDT_INTERRUPT, 0, 1);
    set(145, &interrupt145, IDT_INTERRUPT, 0, 1);
    set(146, &interrupt146, IDT_INTERRUPT, 0, 1);
    set(147, &interrupt147, IDT_INTERRUPT, 0, 1);
    set(148, &interrupt148, IDT_INTERRUPT, 0, 1);
    set(149, &interrupt149, IDT_INTERRUPT, 0, 1);
    set(150, &interrupt150, IDT_INTERRUPT, 0, 1);
    set(151, &interrupt151, IDT_INTERRUPT, 0, 1);
    set(152, &interrupt152, IDT_INTERRUPT, 0, 1);
    set(153, &interrupt153, IDT_INTERRUPT, 0, 1);
    set(154, &interrupt154, IDT_INTERRUPT, 0, 1);
    set(155, &interrupt155, IDT_INTERRUPT, 0, 1);
    set(156, &interrupt156, IDT_INTERRUPT, 0, 1);
    set(157, &interrupt157, IDT_INTERRUPT, 0, 1);
    set(158, &interrupt158, IDT_INTERRUPT, 0, 1);
    set(159, &interrupt159, IDT_INTERRUPT, 0, 1);
    set(160, &interrupt160, IDT_INTERRUPT, 0, 1);
    set(161, &interrupt161, IDT_INTERRUPT, 0, 1);
    set(162, &interrupt162, IDT_INTERRUPT, 0, 1);
    set(163, &interrupt163, IDT_INTERRUPT, 0, 1);
    set(164, &interrupt164, IDT_INTERRUPT, 0, 1);
    set(165, &interrupt165, IDT_INTERRUPT, 0, 1);
    set(166, &interrupt166, IDT_INTERRUPT, 0, 1);
    set(167, &interrupt167, IDT_INTERRUPT, 0, 1);
    set(168, &interrupt168, IDT_INTERRUPT, 0, 1);
    set(169, &interrupt169, IDT_INTERRUPT, 0, 1);
    set(170, &interrupt170, IDT_INTERRUPT, 0, 1);
    set(171, &interrupt171, IDT_INTERRUPT, 0, 1);
    set(172, &interrupt172, IDT_INTERRUPT, 0, 1);
    set(173, &interrupt173, IDT_INTERRUPT, 0, 1);
    set(174, &interrupt174, IDT_INTERRUPT, 0, 1);
    set(175, &interrupt175, IDT_INTERRUPT, 0, 1);
    set(176, &interrupt176, IDT_INTERRUPT, 0, 1);
    set(177, &interrupt177, IDT_INTERRUPT, 0, 1);
    set(178, &interrupt178, IDT_INTERRUPT, 0, 1);
    set(179, &interrupt179, IDT_INTERRUPT, 0, 1);
    set(180, &interrupt180, IDT_INTERRUPT, 0, 1);
    set(181, &interrupt181, IDT_INTERRUPT, 0, 1);
    set(182, &interrupt182, IDT_INTERRUPT, 0, 1);
    set(183, &interrupt183, IDT_INTERRUPT, 0, 1);
    set(184, &interrupt184, IDT_INTERRUPT, 0, 1);
    set(185, &interrupt185, IDT_INTERRUPT, 0, 1);
    set(186, &interrupt186, IDT_INTERRUPT, 0, 1);
    set(187, &interrupt187, IDT_INTERRUPT, 0, 1);
    set(188, &interrupt188, IDT_INTERRUPT, 0, 1);
    set(189, &interrupt189, IDT_INTERRUPT, 0, 1);
    set(190, &interrupt190, IDT_INTERRUPT, 0, 1);
    set(191, &interrupt191, IDT_INTERRUPT, 0, 1);
    set(192, &interrupt192, IDT_INTERRUPT, 0, 1);
    set(193, &interrupt193, IDT_INTERRUPT, 0, 1);
    set(194, &interrupt194, IDT_INTERRUPT, 0, 1);
    set(195, &interrupt195, IDT_INTERRUPT, 0, 1);
    set(196, &interrupt196, IDT_INTERRUPT, 0, 1);
    set(197, &interrupt197, IDT_INTERRUPT, 0, 1);
    set(198, &interrupt198, IDT_INTERRUPT, 0, 1);
    set(199, &interrupt199, IDT_INTERRUPT, 0, 1);
    set(200, &interrupt200, IDT_INTERRUPT, 0, 1);
    set(201, &interrupt201, IDT_INTERRUPT, 0, 1);
    set(202, &interrupt202, IDT_INTERRUPT, 0, 1);
    set(203, &interrupt203, IDT_INTERRUPT, 0, 1);
    set(204, &interrupt204, IDT_INTERRUPT, 0, 1);
    set(205, &interrupt205, IDT_INTERRUPT, 0, 1);
    set(206, &interrupt206, IDT_INTERRUPT, 0, 1);
    set(207, &interrupt207, IDT_INTERRUPT, 0, 1);
    set(208, &interrupt208, IDT_INTERRUPT, 0, 1);
    set(209, &interrupt209, IDT_INTERRUPT, 0, 1);
    set(210, &interrupt210, IDT_INTERRUPT, 0, 1);
    set(211, &interrupt211, IDT_INTERRUPT, 0, 1);
    set(212, &interrupt212, IDT_INTERRUPT, 0, 1);
    set(213, &interrupt213, IDT_INTERRUPT, 0, 1);
    set(214, &interrupt214, IDT_INTERRUPT, 0, 1);
    set(215, &interrupt215, IDT_INTERRUPT, 0, 1);
    set(216, &interrupt216, IDT_INTERRUPT, 0, 1);
    set(217, &interrupt217, IDT_INTERRUPT, 0, 1);
    set(218, &interrupt218, IDT_INTERRUPT, 0, 1);
    set(219, &interrupt219, IDT_INTERRUPT, 0, 1);
    set(220, &interrupt220, IDT_INTERRUPT, 0, 1);
    set(221, &interrupt221, IDT_INTERRUPT, 0, 1);
    set(222, &interrupt222, IDT_INTERRUPT, 0, 1);
    set(223, &interrupt223, IDT_INTERRUPT, 0, 1);
    set(224, &interrupt224, IDT_INTERRUPT, 0, 1);
    set(225, &interrupt225, IDT_INTERRUPT, 0, 1);
    set(226, &interrupt226, IDT_INTERRUPT, 0, 1);
    set(227, &interrupt227, IDT_INTERRUPT, 0, 1);
    set(228, &interrupt228, IDT_INTERRUPT, 0, 1);
    set(229, &interrupt229, IDT_INTERRUPT, 0, 1);
    set(230, &interrupt230, IDT_INTERRUPT, 0, 1);
    set(231, &interrupt231, IDT_INTERRUPT, 0, 1);
    set(232, &interrupt232, IDT_INTERRUPT, 0, 1);
    set(233, &interrupt233, IDT_INTERRUPT, 0, 1);
    set(234, &interrupt234, IDT_INTERRUPT, 0, 1);
    set(235, &interrupt235, IDT_INTERRUPT, 0, 1);
    set(236, &interrupt236, IDT_INTERRUPT, 0, 1);
    set(237, &interrupt237, IDT_INTERRUPT, 0, 1);
    set(238, &interrupt238, IDT_INTERRUPT, 0, 1);
    set(239, &interrupt239, IDT_INTERRUPT, 0, 1);
    set(240, &interrupt240, IDT_INTERRUPT, 0, 1);
    set(241, &interrupt241, IDT_INTERRUPT, 0, 1);
    set(242, &interrupt242, IDT_INTERRUPT, 0, 1);
    set(243, &interrupt243, IDT_INTERRUPT, 0, 1);
    set(244, &interrupt244, IDT_INTERRUPT, 0, 1);
    set(245, &interrupt245, IDT_INTERRUPT, 0, 1);
    set(246, &interrupt246, IDT_INTERRUPT, 0, 1);
    set(247, &interrupt247, IDT_INTERRUPT, 0, 1);
    set(248, &interrupt248, IDT_INTERRUPT, 0, 1);
    set(249, &interrupt249, IDT_INTERRUPT, 0, 1);
    set(250, &interrupt250, IDT_INTERRUPT, 0, 1);
    set(251, &interrupt251, IDT_INTERRUPT, 0, 1);
    set(252, &interrupt252, IDT_INTERRUPT, 0, 1);
    set(253, &interrupt253, IDT_INTERRUPT, 0, 1);
    set(254, &interrupt254, IDT_INTERRUPT, 0, 1);
    set(255, &interrupt255, IDT_INTERRUPT, 0, 1);
}

fn load() void {
    interrupt_table_descriptor.size = 256 * 16 - 1;
    interrupt_table_descriptor.offset = @ptrToInt(&interrupt_table);

    asm volatile (
        \\.intel_syntax noprefix
        \\lidt qword ptr [rax]
        \\.att_syntax prefix
        :
        : [idtr] "{rax}" (&interrupt_table_descriptor),
    );
}

const GeneralRegisters = packed struct {
    r15: usize,
    r14: usize,
    r13: usize,
    r12: usize,
    r11: usize,
    r10: usize,
    r9: usize,
    r8: usize,
    rdi: usize,
    rsi: usize,
    rbp: usize,
    rsp: usize,
    rbx: usize,
    rdx: usize,
    rcx: usize,
    rax: usize,
};

const SegmentRegisters = packed struct {
    es: usize,
    cs: usize,
    ss: usize,
    ds: usize,
    fs: usize,
    gs: usize,
};

const Context = packed struct {
    segment_registers: SegmentRegisters,
    general_registers: GeneralRegisters,
    intn: usize,
    error_code: usize,
    ret_addr: usize,
    code_selector: usize,
    eflags: usize,
};

fn dump_context(context: *Context) callconv(.C) void {
    term.printf("interrupt: {X:0>2}\r\n", .{context.intn});
    term.printf("error code: {X:2>0}\r\n", .{context.error_code});
    term.printf(
        \\r15={X:0>16}h r14={X:0>16}h r13={X:0>16}h es={X:0>4}h 
        \\r12={X:0>16}h r11={X:0>16}h r10={X:0>16}h cs={X:0>4}h
        \\r9 ={X:0>16}h r8 ={X:0>16}h rdi={X:0>16}h ss={X:0>4}h
        \\rsi={X:0>16}h rbp={X:0>16}h rsp={X:0>16}h ds={X:0>4}h
        \\rbx={X:0>16}h rdx={X:0>16}h rcx={X:0>16}h fs={X:0>4}h
        \\rax={X:0>16}h rip={X:0>16}h                       gs={X:0>4}h
        \\gdt={X:0>16}h idt={X:0>16}h
        \\cr2={X:0>16}h
        \\eflags={X:0>16}h
    , .{ context.general_registers.r15, context.general_registers.r14, context.general_registers.r13, context.segment_registers.es, context.general_registers.r12, context.general_registers.r11, context.general_registers.r10, context.segment_registers.cs, context.general_registers.r9, context.general_registers.r8, context.general_registers.rdi, context.segment_registers.ss, context.general_registers.rsi, context.general_registers.rbp, context.general_registers.rsp, context.segment_registers.ds, context.general_registers.rbx, context.general_registers.rdx, context.general_registers.rcx, context.segment_registers.fs, context.general_registers.rax, context.ret_addr, context.segment_registers.gs, arch.read_gdtr64().offset, arch.read_idtr64().offset, arch.read_cr2(), context.eflags });
}

const serial = @import("serial.zig");

pub export fn handle_interrupt(context: *Context) callconv(.C) void {
    switch (context.intn) {
        0x06, 0x0E => {
            dump_context(context);
        },
        pic.PRIMARY_PIC_VECTOR + 4 => {
            const idx = serial.write.*;

            while (pio.inb(serial.com1 + 5) & 1 == 0) {}
            const ch = pio.inb(serial.com1);

            serial.buffer[idx] = ch;
            serial.write.* = (idx + 1) % serial.buffer.len;
        },
        else => {},
    }

    switch (context.intn) {
        pic.PRIMARY_PIC_VECTOR...pic.PRIMARY_PIC_VECTOR + 15 => {
            pic.eoi(context.intn);
        },
        else => {},
    }
}
