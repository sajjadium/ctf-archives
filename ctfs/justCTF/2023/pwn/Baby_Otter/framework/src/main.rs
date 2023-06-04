use std::env;
use std::fmt;
use std::thread;
use std::mem::drop;
use std::path::Path;
use std::error::Error;
use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};

use sui_ctf_framework::NumericalAddress;
use sui_transactional_test_runner::args::SuiValue;
use sui_transactional_test_runner::test_adapter::FakeID;

fn handle_client(mut stream: TcpStream) -> Result<(), Box<dyn Error>> {

    // Initialize SuiTestAdapter
    let chall = "baby_otter_challenge";
    let named_addresses = vec![
        ("challenge".to_string(), NumericalAddress::parse_str("0x8107417ed30fcc2d0b0dfd680f12f6ead218cb971cb989afc8d28ad37da89467")?),
        ("solution".to_string(), NumericalAddress::parse_str("0x42f5c1c42496636b461f1cb4f8d62aac8ebac3ca7766c154b63942671bc86836")?),
    ];
    
    let precompiled = sui_ctf_framework::get_precompiled(Path::new(&format!(
        "./chall/build/{}/sources/dependencies",
        chall
    )));

    let mut adapter = sui_ctf_framework::initialize(
        named_addresses,
        &precompiled,
        Some(vec!["challenger".to_string(), "solver".to_string()]),
    );
    
    let mut solution_data = [0 as u8; 1000]; 
    let _solution_size = stream.read(&mut solution_data)?;

    // Publish Challenge Module
    let mod_bytes: Vec<u8> = std::fs::read(format!(
        "./chall/build/{}/bytecode_modules/{}.mv",
        chall, chall
    ))?;
    let chall_dependencies: Vec<String> = Vec::new();
    let chall_addr = sui_ctf_framework::publish_compiled_module(&mut adapter, mod_bytes, chall_dependencies, Some(String::from("challenger")));
    println!("[SERVER] Challenge published at: {:?}", chall_addr);

    // Publish Solution Module
    let mut sol_dependencies: Vec<String> = Vec::new();
    sol_dependencies.push(String::from("challenge"));
    let sol_addr = sui_ctf_framework::publish_compiled_module(&mut adapter, solution_data.to_vec(), sol_dependencies, Some(String::from("solver")));
    println!("[SERVER] Solution published at: {:?}", sol_addr);

    let mut output = String::new();
    fmt::write(
        &mut output,
        format_args!(
            "[SERVER] Challenge published at {}. Solution published at {}",
            chall_addr.to_string().as_str(),
            sol_addr.to_string().as_str()
        ),
    ).unwrap();
    stream.write(output.as_bytes()).unwrap();

    // Prepare Function Call Arguments
    let mut args_sol : Vec<SuiValue> = Vec::new();
    let arg_ob = SuiValue::Object(FakeID::Enumerated(1, 1));
    args_sol.push(arg_ob);

    // Call solve Function
    let ret_val = sui_ctf_framework::call_function(
        &mut adapter,
        sol_addr,
        "baby_otter_solution",
        "solve",
        args_sol,
        Some("solver".to_string())
    );
    println!("[SERVER] Return value {:#?}", ret_val);
    println!("");

    // Check Solution
    let mut args2: Vec<SuiValue> = Vec::new();
    let arg_ob2 = SuiValue::Object(FakeID::Enumerated(1, 1));
    args2.push(arg_ob2);

    let ret_val = sui_ctf_framework::call_function(
        &mut adapter,
        chall_addr,
        chall,
        "is_owner",
        args2,
        Some("challenger".to_string()),
    );
    println!("[SERVER] Return value {:#?}", ret_val);
    println!("");

    // Validate Solution
    match ret_val {
        Ok(()) => {
            println!("[SERVER] Correct Solution!");
            println!("");
            if let Ok(flag) = env::var("FLAG") {
                let message = format!("[SERVER] Congrats, flag: {}", flag);
                stream.write(message.as_bytes()).unwrap();
            } else {
                stream.write("[SERVER] Flag not found, please contact admin".as_bytes()).unwrap();
            }
        }
        Err(_error) => {
            println!("[SERVER] Invalid Solution!");
            println!("");
            stream.write("[SERVER] Invalid Solution!".as_bytes()).unwrap();
        }
    };

    Ok(())
}

fn main() -> Result<(), Box<dyn Error>> {

    // Create Socket - Port 31337
    let listener = TcpListener::bind("0.0.0.0:31337")?;
    println!("[SERVER] Starting server at port 31337!");

    // Wait For Incoming Solution
    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                println!("[SERVER] New connection: {}", stream.peer_addr().unwrap());
                thread::spawn(move|| handle_client(stream).unwrap());
            }
            Err(e) => {
                println!("[SERVER] Error: {}", e);
            }
        }        
    }

    // Close Socket Server
    drop(listener);
    Ok(())
}
