use actix_files::NamedFile;
use actix_multipart::Multipart;
use actix_web::cookie::Cookie;
use actix_web::http::StatusCode;
use actix_web::{get, post, App, HttpRequest, HttpResponse, HttpServer, Responder, Result};
use futures_util::stream::TryStreamExt;
use futures_util::StreamExt;
use rand::{thread_rng, RngCore};
use std::collections::hash_map::DefaultHasher;
use std::fs::create_dir_all;
use std::hash::{Hash, Hasher};
use std::io::{ErrorKind, SeekFrom};
use std::path::PathBuf;
use std::str::FromStr;
use tokio::fs::{remove_file, write, File, OpenOptions};
use tokio::io::AsyncReadExt;
use tokio::io::{copy, AsyncSeekExt};
use tokio_util::io::StreamReader;

async fn handle_multipart(user_dir: &PathBuf, mut multipart: Multipart) -> Result<()> {
    let mut count = 0;

    // optimised from: https://github.com/actix/examples/blob/db5f00e771573023a1d3de402f47a661c5799ec9/forms/multipart/src/main.rs#L8
    while let Some(field) = multipart.try_next().await? {
        count += 1;
        if count > 16 {
            return Err(std::io::Error::new(
                ErrorKind::InvalidInput,
                "Too many files provided in input!",
            )
            .into());
        }
        let content_disposition = field.content_disposition();

        if let Some(filename) = content_disposition.get_filename() {
            let mut hasher = DefaultHasher::new();
            filename.hash(&mut hasher);
            let mut tmp = PathBuf::from_str("tmp/").unwrap();
            tmp.push(format!("{:016x}", hasher.finish()));

            let mut file = OpenOptions::new()
                .read(true)
                .write(true)
                .create(true)
                .open(&tmp)
                .await?;

            let mut freader = StreamReader::new(field.map(|result| {
                // StreamReader-friendly
                result.map_err(|err| std::io::Error::new(ErrorKind::Other, err))
            }))
            .take(1 << 16); // max file size

            copy(&mut freader, &mut file).await?;

            // upload succeeded; copy to user area
            let destination = user_dir.join(
                tmp.file_name()
                    .expect("Must be present based on filename creation."),
            );

            // avoid overhead from open()
            file.seek(SeekFrom::Start(0)).await?;
            let mut orig = file;
            let mut dest = File::create(&destination).await?;

            copy(&mut orig, &mut dest).await?;

            // cleanup
            drop(orig);
            drop(dest);
            remove_file(tmp).await?;
        } else {
            return Err(std::io::Error::new(
                ErrorKind::InvalidInput,
                "Missing filename from provided file.".to_string(),
            )
            .into());
        }
    }
    Ok(())
}

#[post("/")]
async fn upload(req: HttpRequest, multipart: Multipart) -> Result<HttpResponse> {
    if let Some(user) = req.cookie("whoami") {
        let mut hasher = DefaultHasher::new();
        user.value().hash(&mut hasher);
        let user_dir = PathBuf::from(format!("user/{:016x}", hasher.finish()));
        create_dir_all(&user_dir)?;

        if let Err(e) = handle_multipart(&user_dir, multipart).await {
            write(user_dir.join("error"), e.to_string()).await?;
        }

        let mut body = Vec::new();
        let mut tar = tar::Builder::new(&mut body);
        tar.append_dir_all("submitted", user_dir)?;
        drop(tar);
        Ok(HttpResponse::build(StatusCode::OK)
            .content_type("application/tar")
            .insert_header(("Content-Disposition", "attachment"))
            .body(body)
            .respond_to(&req)
            .map_into_boxed_body())
    } else {
        Ok(HttpResponse::new(StatusCode::UNAUTHORIZED))
    }
}

#[get("/")]
async fn index(req: HttpRequest) -> Result<HttpResponse> {
    let mut res = NamedFile::open("www/index.html")?.into_response(&req);
    if req.cookie("whoami").is_none() {
        let mut rng = thread_rng();
        let mut ident = [0u8; 256]; // big un-bruteforce-able bytes
        rng.fill_bytes(&mut ident);
        res.add_cookie(
            &Cookie::build("whoami", hex::encode(ident))
                .http_only(true)
                .finish(),
        )?;
    }
    Ok(res)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let addr = std::env::var("SERVER_ADDR")
        .expect("Couldn't find an appropriate server address; did you set SERVER_ADDR?");
    HttpServer::new(|| App::new().service(index).service(upload))
        .bind_uds(addr)?
        .run()
        .await
}
