use fmt;
use bufio;
use bytes;
use os;
use strings;
use unix::signal;

const bufsz: u8 = 8;

type note = struct {
    title: [32]u8,
    content: [128]u8,
    init: bool,
};

fn ptr_forward(p: *u8) void = {
    if (*p == bufsz - 1) {
        fmt::println("error: out of bounds seek")!;
    } else {
        *p += 1;
    };
    return;
};

fn ptr_back(p: *u8) void = {
    if (*p - 1 < 0) {
        fmt::println("error: out of bounds seek")!;
    } else {  
        *p -= 1;
    };
    return;
};

fn note_add(note: *note) void = {
    fmt::print("enter your note title: ")!;
    bufio::flush(os::stdout)!;
    let title = bufio::scanline(os::stdin)! as []u8;
    let sz = if (len(title) >= len(note.title)) len(note.title) else len(title);
    note.title[..sz] = title[..sz];
    free(title);
    
    fmt::print("enter your note content: ")!;
    bufio::flush(os::stdout)!;
    let content = bufio::scanline(os::stdin)! as []u8;
    sz = if (len(content) >= len(note.content)) len(note.content) else len(content);
    note.content[..sz] = content[..sz];
    free(content);   
    note.init = true;
};

fn note_delete(note: *note) void = {
    if (!note.init) {
        fmt::println("error: no note at this location")!;
        return;
    };
    bytes::zero(note.title);
    bytes::zero(note.content);
    note.init = false;
    return;
};

fn note_read(note: *note) void = {
    if (!note.init) {
        fmt::println("error: no note at this location")!;
        return;
    };
    fmt::printfln("title: {}\ncontent: {}",
        strings::fromutf8_unsafe(note.title),
        strings::fromutf8_unsafe(note.content)
    )!;
    return;
};

fn handler(sig: int, info: *signal::siginfo, ucontext: *void) void = {
  fmt::println("goodbye :)")!;
  os::exit(1);
};

export fn main() void = {
    signal::handle(signal::SIGINT, &handler);
    let idx: u8 = 0;
    let opt: []u8 = [];
    let notes: [8]note = [
            note { title = [0...], content = [0...], init = false}...
    ];
    let notep: *[*]note = &notes;
    assert(bufsz == len(notes));
    for (true) {
        fmt::printf(
"1) Move note pointer forward
2) Move note pointer backward
3) Add note
4) Delete note
5) Read note
6) Exit
> ")!;
        bufio::flush(os::stdout)!;
        opt = bufio::scanline(os::stdin)! as []u8;
        defer free(opt);
        switch (strings::fromutf8(opt)!) {
            case "1" => ptr_forward(&idx);
            case "2" => ptr_back(&idx);
            case "3" => note_add(&notep[idx]);
            case "4" => note_delete(&notep[idx]);
            case "5" => note_read(&notep[idx]);
            case "6" => break;
            case => fmt::println("Invalid option")!;
        };
    };
};

