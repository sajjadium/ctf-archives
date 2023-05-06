use std::{
    error::Error,
    io::{stdin, Read},
    process::{exit, Command, Stdio},
    result::Result,
    thread,
    vec::Vec,
};

fn main() -> Result<(), Box<dyn Error>> {
    let mut buffer = String::new();
    println!("Enter an IP address: ");
    stdin().read_line(&mut buffer)?;

    let ips: Vec<&str> = buffer.trim().split('.').collect();

    assert!(ips.len() == 4);

    let mut ip_nums = Vec::new();

    for num in ips.into_iter() {
        let num = num.parse::<u8>()?;
        ip_nums.push(num);
    }

    let format_ip = format!(
        "{}.{}.{}.{}",
        ip_nums[0], ip_nums[1], ip_nums[2], ip_nums[3]
    );

    let mut child = Command::new("xvfb-run")
        .args(["./teeworlds", &format!("connect {}", format_ip)])
        .stderr(Stdio::inherit())
        .stdout(Stdio::inherit())
        .stdin(Stdio::null())
        .spawn()
        .expect("failed to execute process");

    let _handle = thread::spawn(|| {
        let mut buffer = [0; 100];
        loop {
            if let Ok(re) = stdin().read(&mut buffer) {
                if re == 0 {
                    exit(0);
                }
            } else {
                exit(0);
            }
        }
    });

    child.wait()?;
    Ok(())
}
