fn IO_return(val) {
    let {
        f(rw) = {|rw(), val()},
    } in {|f}
}

fn main() {
    IO_return({|})
}
