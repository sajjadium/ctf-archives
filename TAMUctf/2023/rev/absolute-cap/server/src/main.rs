use anyhow::Result;

use nix::fcntl::{fcntl, FcntlArg, OFlag, SealFlag};
use nix::sys::memfd::{memfd_create, MemFdCreateFlag};
use nix::unistd::Uid;
use std::ffi::CString;
use std::fs::Permissions;
use std::net::SocketAddr;
use std::os::fd::{AsRawFd, FromRawFd};
use std::os::unix::fs::PermissionsExt;
use std::process::Stdio;
use tokio::fs::File;
use tokio::io::{copy, AsyncBufReadExt, AsyncReadExt, AsyncWriteExt, BufReader, BufWriter};
use tokio::net::{TcpListener, TcpStream};
use tokio::process::Command;
use tokio::{pin, select};

async fn handle_client(mut client: TcpStream, source: SocketAddr) -> Result<()> {
    println!("Handling connection from: {source}");

    let stream_fd = client.as_raw_fd();

    let (rx, tx) = client.split();
    let mut rx = BufReader::new(rx);
    let mut tx = BufWriter::new(tx);

    while let Ok(Some(line)) = (&mut rx).lines().next_line().await {
        let line = line.trim();
        if line == "execute" {
            tx.write_all(b"size of file: ").await?;
            tx.flush().await?;
            if let Ok(Some(bytes)) = (&mut rx).lines().next_line().await {
                if let Ok(bytes) = bytes.parse() {
                    if bytes > 4 << 20 {
                        tx.write_all(b"Cowardly refusing to create a binary >4MB.")
                            .await?;
                        tx.flush().await?;
                        continue;
                    }

                    let memfd = memfd_create(
                        CString::new(format!("{source}"))?.as_c_str(),
                        MemFdCreateFlag::MFD_CLOEXEC | MemFdCreateFlag::MFD_ALLOW_SEALING,
                    )?;

                    let file = unsafe { File::from_raw_fd(memfd) };
                    let mut writer = BufWriter::new(file);
                    copy(&mut (&mut rx).take(bytes), &mut writer).await?;
                    let file = writer.into_inner();

                    // prevent further writing
                    file.set_permissions(Permissions::from_mode(0o555)).await?;
                    fcntl(memfd, FcntlArg::F_ADD_SEALS(SealFlag::all()))?;

                    let executable = format!("/proc/self/fd/{memfd}");
                    println!("Launching {executable} for {source}");

                    let fut_status = Command::new(executable)
                        .stdin(unsafe { Stdio::from_raw_fd(stream_fd) })
                        .stdout(unsafe { Stdio::from_raw_fd(stream_fd) })
                        .stderr(unsafe { Stdio::from_raw_fd(stream_fd) })
                        .env_clear()
                        .uid(Uid::current().as_raw() + 1000)
                        .kill_on_drop(true)
                        .status();
                    pin!(fut_status);

                    let status = loop {
                        // loop until the process ends or the stream is killed
                        select! {
                            status = &mut fut_status => break status?,
                            readable = rx.get_mut().readable() => readable?,
                        }
                    };

                    tx.write_all(
                        format!("Execute complete; exited {:?}\n", status.code()).as_bytes(),
                    )
                    .await?;
                    tx.flush().await?;
                } else {
                    tx.write_all(b"Invalid length specified: ").await?;
                    tx.write_all(bytes.as_bytes()).await?;
                    tx.write_u8(b'\n').await?;
                    tx.flush().await?;
                }
            }
        } else {
            tx.write_all(b"Didn't recognise command. Try again?\n")
                .await?;
            tx.flush().await?;
        }
    }

    println!("Mischief managed for {source}!");

    Ok(())
}

async fn run_server() -> Result<()> {
    let server = TcpListener::bind("0.0.0.0:16983").await?;
    println!("{}", server.local_addr()?);

    while let Ok((conn, source)) = server.accept().await {
        fcntl(conn.as_raw_fd(), FcntlArg::F_SETFL(OFlag::O_CLOEXEC))?;
        tokio::spawn(async move {
            if let Err(e) = handle_client(conn, source).await {
                println!("Encountered error while handling {source}: {e}");
            }
        });
    }

    Ok(())
}

fn main() -> Result<()> {
    tokio::runtime::Builder::new_current_thread()
        .enable_all()
        .build()
        .unwrap()
        .block_on(run_server())
}
