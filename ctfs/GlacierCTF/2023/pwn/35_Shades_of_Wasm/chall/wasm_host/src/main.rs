use anyhow::anyhow;
use base64::{engine::general_purpose as base64_engine, Engine as _};
use wasmtime::*;
use wasmtime_wasi::sync::WasiCtxBuilder;

fn main() -> anyhow::Result<()> {
    let mut config = Config::new();

    config.debug_info(false);
    config.cranelift_debug_verifier(false);

    config.strategy(Strategy::Cranelift);
    config.cranelift_opt_level(OptLevel::SpeedAndSize);

    config.static_memory_forced(true);

    let engine = Engine::new(&config)?;
    let mut linker = Linker::new(&engine);

    wasmtime_wasi::add_to_linker(&mut linker, |s| s)?;

    let wasi = WasiCtxBuilder::new().inherit_stdio().build();

    let mut store = Store::new(&engine, wasi);

    println!("Enter your module in base64:");
    let user_module_wat = {
        let stdin = std::io::stdin();
        let mut user_module_wat = String::new();
        stdin.read_line(&mut user_module_wat)?;

        let user_module_wat = user_module_wat
            .strip_suffix("\n")
            .unwrap_or(&user_module_wat);

        match base64_engine::STANDARD.decode(&user_module_wat) {
            Ok(user_module_wat) => user_module_wat,
            Err(_) => return Err(anyhow!("invalid base64")),
        }
    };

    let user_module = match Module::new(&engine, user_module_wat) {
        Ok(user_module) => user_module,
        Err(_) => return Err(anyhow!("invalid module")),
    };

    let _ = linker.module(&mut store, "module", &user_module)?;

    linker
        .get_default(&mut store, "module")?
        .typed::<(), ()>(&store)?
        .call(&mut store, ())?;

    Ok(())
}
