use std::process;

use actix_session::{storage::CookieSessionStore, Session, SessionMiddleware};
use actix_web::{
    cookie::Key,
    get, post,
    web::{self, Redirect},
    App, HttpServer, Responder,
};
use base64::prelude::{Engine as _, BASE64_STANDARD};
use maud::{html, Markup, DOCTYPE};
use rand::Rng;
use redis::{aio::MultiplexedConnection, AsyncCommands};
use redis_derive::FromRedisValue;
use serde::Deserialize;

#[derive(Debug, derive_more::Display, derive_more::From)]
enum Error {
    #[display("Valkey: {}", _0)]
    Valkey(redis::RedisError),
    Internal(Box<dyn std::error::Error>),
    Unauthorized,
    NotFound,
    PaymentRequired,
}

impl actix_web::error::ResponseError for Error {
    fn status_code(&self) -> actix_web::http::StatusCode {
        match self {
            Error::Unauthorized => actix_web::http::StatusCode::UNAUTHORIZED,
            Error::NotFound => actix_web::http::StatusCode::NOT_FOUND,
            Error::PaymentRequired => actix_web::http::StatusCode::PAYMENT_REQUIRED,
            _ => actix_web::http::StatusCode::INTERNAL_SERVER_ERROR,
        }
    }
}

#[derive(Debug, FromRedisValue)]
struct Article {
    title: String,
    image: Option<String>,
    contents: String,
    author: String,
    published: bool,
}

fn layout(contents: Markup) -> Markup {
    html! {
        (DOCTYPE)
        head lang="en" {
            title { "Articular" }
            meta charset="utf-8";
        }
        body {
            (contents)
        }
    }
}

#[get("/")]
async fn index(db: web::Data<redis::Client>) -> Result<Markup, Error> {
    let mut conn = db.get_multiplexed_async_connection().await?;
    let mut cursor: redis::AsyncIter<String> = conn.scan_match("article:*").await?;
    let mut keys = vec![];
    while let Some(key) = cursor.next_item().await {
        keys.push(key);
    }
    drop(cursor);
    let mut articles = Vec::<(String, Article)>::with_capacity(keys.len());
    for key in keys.iter() {
        let article: Article = conn.hgetall(key).await?;
        if article.published {
            articles.push((key.strip_prefix("article:").unwrap().to_string(), article));
        }
    }

    Ok(layout(html! {
        h1 { "Articles" }
        ul {
            @for (id, article) in articles {
                li {
                    a href={ "/article/" (id) } {
                        (article.title)
                    }
                }
            }
        }
        a href="/mine" { "Show my articles" }
    }))
}

#[get("/article/{id}")]
async fn show(
    db: web::Data<redis::Client>,
    id: web::Path<u64>,
    session: Session,
) -> Result<Markup, Error> {
    let mut conn = db.get_multiplexed_async_connection().await?;
    let Ok(article) = conn.hgetall::<_, Article>(format!("article:{}", id)).await else {
        return Err(Error::NotFound);
    };
    if !article.published && article.author != get_user(&session) {
        return Err(Error::Unauthorized);
    }
    Ok(layout(html! {
        h1 { (article.title) }
        p {
            "By " (article.author)
            @if !article.published {
                " (draft)"
            }
        }
        @if let Some(image) = article.image {
            img height="400" src=(image);
        }
        pre { (article.contents) }
    }))
}

#[get("/article/{id}/write")]
async fn write_form(
    db: web::Data<redis::Client>,
    session: Session,
    id: web::Path<String>,
) -> Result<Markup, Error> {
    let mut conn = db.get_multiplexed_async_connection().await?;
    let article: Option<Article> = if *id == "new" {
        None
    } else {
        let article: Article = conn.hgetall(format!("article:{}", id)).await?;
        if article.author != get_user(&session) {
            return Err(Error::Unauthorized);
        }
        Some(article)
    };
    let published = article.as_ref().is_some_and(|a| a.published);

    Ok(layout(html! {
        h1 { "New article" }
        form method="post" action={ "/article" @if *id != "new" { "/" (id) } } {
            label for="title" { "Title" }
            input type="text" name="title" id="title" value=[article.as_ref().map(|a| &a.title)];

            br;

            label for="img-url" { "Image link" @if *id != "new" { " (leave empty to keep)" } }
            input type="text" name="img-url" id="img-url";
            @if let Some(article) = &article {
                @if let Some(image) = &article.image {
                    br;
                    img height="200" src=(image);
                }
            }

            br;

            label for="contents" { "Contents" }
            textarea name="contents" id="contents" {
                @if let Some(article) = &article {
                    (article.contents)
                }
            }

            br;

            button name="published" value="false" { @if published { "Unpublish to draft" } @else { "Save draft" } }
            button name="published" value="true" { @if published { "Save" } @else { "Publish" } }
        }
    }))
}

#[derive(Debug, Deserialize)]
struct ArticleForm {
    title: String,
    #[serde(rename = "img-url")]
    img_url: String,
    contents: String,
    published: bool,
}

#[post("/article")]
async fn new_article(
    db: web::Data<redis::Client>,
    form: web::Form<ArticleForm>,
    session: Session,
) -> Result<impl Responder, Error> {
    let author = get_user(&session);
    let mut conn = db.get_multiplexed_async_connection().await?;
    let id = conn.incr::<_, _, u64>("article_id_counter", 1).await?;
    let form = form.0;
    set_article(
        &mut conn,
        id,
        Article {
            title: form.title,
            image: get_image(&form.img_url)?,
            contents: form.contents,
            author,
            published: form.published,
        },
    )
    .await?;
    Ok(Redirect::to(format!("/article/{}", id)).see_other())
}

#[post("/article/{id}")]
async fn update_article(
    db: web::Data<redis::Client>,
    id: web::Path<u64>,
    form: web::Form<ArticleForm>,
    session: Session,
) -> Result<impl Responder, Error> {
    let author = get_user(&session);
    let mut conn = db.get_multiplexed_async_connection().await?;
    let article_author: String = conn.hget(format!("article:{}", id), "author").await?;
    if author != article_author {
        return Err(Error::Unauthorized);
    }
    let form = form.0;
    set_article(
        &mut conn,
        *id,
        Article {
            title: form.title,
            contents: form.contents,
            author,
            image: get_image(&form.img_url)?,
            published: form.published,
        },
    )
    .await?;
    Ok(Redirect::to(format!("/article/{}", id)).see_other())
}

fn get_image(url: &str) -> Result<Option<String>, Error> {
    if url.is_empty() {
        return Ok(None);
    }
    if !regex::Regex::new(r"https?://.*").unwrap().is_match(url) {
        return Ok(None);
    }
    process::Command::new("curl")
        .arg("-q")
        .arg(url)
        .output()
        .map(|output| {
            let mut s = "data:image/png;base64,".to_string();
            BASE64_STANDARD.encode_string(output.stdout, &mut s);
            Some(s)
        })
        .map_err(|e| Error::Internal(Box::new(e)))
}

async fn set_article(
    conn: &mut MultiplexedConnection,
    id: u64,
    article: Article,
) -> Result<(), Error> {
    if article.published {
        return Err(Error::PaymentRequired);
    }
    let mut items: Vec<(&str, &str)> = vec![
        ("title", &article.title),
        ("contents", &article.contents),
        ("author", &article.author),
        ("published", if article.published { "1" } else { "0" }),
    ];
    if let Some(image) = &article.image {
        items.push(("image", image));
    }
    () = conn.hset_multiple(format!("article:{}", id), &items)
        .await?;
    Ok(())
}

#[get("/mine")]
async fn mine(db: web::Data<redis::Client>, session: Session) -> Result<Markup, Error> {
    let mut conn = db.get_multiplexed_async_connection().await?;
    let mut cursor: redis::AsyncIter<String> = conn.scan_match("article:*").await?;
    let mut keys = vec![];
    while let Some(key) = cursor.next_item().await {
        keys.push(key);
    }
    drop(cursor);
    let mut articles = Vec::<(String, Article)>::with_capacity(keys.len());
    for key in keys.iter() {
        let article: Article = conn.hgetall(key).await?;
        if article.author == get_user(&session) {
            articles.push((key.strip_prefix("article:").unwrap().to_string(), article));
        }
    }
    Ok(layout(html! {
        h1 { "Your articles" }
        ul {
            @for (id, article) in articles {
                li {
                    a href={ "/article/" (id) } {
                        (article.title)
                    }
                    a href={ "/article/" (id) "/write" } {
                        "✎"
                    }
                }
            }
        }
        a href="/article/new/write" { "Write new" }
        br;
        a href="/" { "View all articles" }
    }))
}

fn get_user(session: &Session) -> String {
    match session.get("userid") {
        Ok(Some(id)) => id,
        _ => {
            let mut rng = rand::thread_rng();
            let id: String = (0..20).map(|_| rng.gen_range('a'..='z')).collect();
            session.insert("userid", &id).unwrap();
            id
        }
    }
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let client = redis::Client::open("redis://valkey:6379/").unwrap();
    let secret_key = Key::from(&(0..64).map(|_| rand::random()).collect::<Vec<u8>>());
    HttpServer::new(move || {
        App::new()
            .wrap(
                SessionMiddleware::builder(CookieSessionStore::default(), secret_key.clone())
                    .cookie_secure(false)
                    .build(),
            )
            .service(index)
            .service(show)
            .service(write_form)
            .service(new_article)
            .service(update_article)
            .service(mine)
            .app_data(web::Data::new(client.clone()))
    })
    .bind(("0.0.0.0", 25565))?
    .run()
    .await
}
