use std::net::TcpStream;
use std::io::{Read, Write};
use std::str::from_utf8;
use std::{error::Error, fs};
use std::env;

fn main() -> Result<(), Box<dyn Error>> {

    let host = env::var("HOST").unwrap_or_else(|_| "127.0.0.1".to_string());
    let port = env::var("PORT").unwrap_or_else(|_| "31337".to_string());

    match TcpStream::connect(format!("{}:{}", host, port)) {
        Ok(mut stream) => {
            println!("  - Connected!");

            let mod_data : Vec<u8> = fs::read("./solve/build/baby_otter_solution/bytecode_modules/baby_otter_solution.mv").unwrap();
            println!("  - Loaded solution!");

            stream.write_all(&mod_data)?;
            stream.flush()?;
            println!("  - Sent solution!");

            let mut return_data = [0 as u8; 200];
            match stream.read(&mut return_data) {
                Ok(_) => {
                    println!("  - Connection Output: '{}'", from_utf8(&return_data).unwrap()); // Get module address
                    let mut flag = [0 as u8; 200]; 
                    match stream.read(&mut flag) {
                        Ok(_) => {
                            println!("  - Connection Output: '{}'", from_utf8(&flag).unwrap()); // Get flag

                        },
                        Err(e) => {
                            println!("  - Failed to receive data: {}", e);
                        }
                    }
                },
                Err(e) => {
                    println!("  - Failed to receive data: {}", e);
                }
            }
        },
        Err(e) => {
            println!("  - Failed to connect: {}", e);
        }
    }
    println!("  - Terminated.");

    Ok(())
}
