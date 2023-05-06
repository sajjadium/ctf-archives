use sm_ext::{c_str, forwards, native, register_natives, ExecType, IExtension, IExtensionInterface, IForwardManager, IPluginContext, IShareSys, SMExtension};
use std::ffi::{CStr, CString};
use std::fs::File;
use std::io::prelude::*;

#[forwards]
struct SQForwards {
    #[global_forward("OnDownloaded", ExecType::Single)]
    on_rust_call: fn(fname: &CStr) -> (),

    #[global_forward("notify", ExecType::Single)]
    on_rust_notify: fn(fname: &CStr) -> (),
}

fn notify(msg: &str) -> Result<(), sm_ext::SPError> {
    let cstr = CString::new(msg).expect("CStr::from_bytes_with_nul failed");
    let result = SQForwards::on_rust_notify(|fwd| fwd.execute(&cstr))?;
    Ok(result)
}

fn download_and_save(url: &str) -> Result<(), String> {
    let resp = reqwest::blocking::get(url).map_err(|_|format!("Failed to get content of {}", url))?.text().map_err(|_|"Failed to get text")?;
    let mut file = File::create("./csgo/scripts/vscripts/test.nut").map_err(|_|"Failed to create script file")?;
    file.write_all(resp.as_bytes()).map_err(|_|"Failed to write script to disk")?;
    Ok(())
}

#[native]
fn native_call(_ctx: &IPluginContext, a: &CStr) -> Result<(), sm_ext::SPError> {
    let result = download_and_save(&*a.to_string_lossy());
    match result {
        Ok(())=>{
            SQForwards::on_rust_call(|fwd| fwd.execute(c_str!("test.nut")))
        }
        Err(s)=>{
            notify(&s)
        }
    }
}

#[derive(Default, SMExtension)]
#[extension(name = "SQExt", description = "Execute squirrel code")]
pub struct SQExtension;

impl IExtensionInterface for SQExtension {
    fn on_extension_load(&mut self, myself: IExtension, sys: IShareSys, _late: bool) -> Result<(), Box<dyn std::error::Error>> {
        let forward_manager: IForwardManager = sys.request_interface(&myself)?;

        SQForwards::register(&forward_manager)?;

        register_natives!(&sys, &myself, [("call", native_call),]);

        Ok(())
    }

    fn on_extension_unload(&mut self) {
        SQForwards::unregister();
    }
}
