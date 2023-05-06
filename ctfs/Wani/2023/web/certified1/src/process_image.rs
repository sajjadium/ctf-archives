use anyhow::{bail, Context, Result};
use std::path::Path;
use std::process::Stdio;
use tokio::fs;
use tokio::process::Command;

pub async fn process_image(working_directory: &Path, input_filename: &Path) -> Result<()> {
    fs::copy(
        working_directory.join(input_filename),
        working_directory.join("input"),
    )
    .await
    .context("Failed to prepare input")?;

    fs::write(
        working_directory.join("overlay.png"),
        include_bytes!("../assets/hanko.png"),
    )
    .await
    .context("Failed to prepare overlay")?;

    let child = Command::new("sh")
        .args([
            "-c",
            "timeout --signal=KILL 5s magick ./input -resize 640x480 -compose over -gravity southeast ./overlay.png -composite ./output.png",
        ])
        .current_dir(working_directory)
        .stdin(Stdio::null())
        .stdout(Stdio::null())
        .stderr(Stdio::piped())
        .spawn()
        .context("Failed to spawn")?;

    let out = child
        .wait_with_output()
        .await
        .context("Failed to read output")?;

    if !out.status.success() {
        bail!(
            "image processing failed on {}:\n{}",
            working_directory.display(),
            std::str::from_utf8(&out.stderr)?
        );
    }

    Ok(())
}
