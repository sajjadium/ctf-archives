use rand::seq::SliceRandom;
use std::collections::HashMap;
use std::sync::{Arc, RwLock};
use tide::{Request, Redirect, Response};
use tide::prelude::*;

#[derive(Clone)]
struct State {
    value: Arc<RwLock<HashMap<String, String>>>
}

impl State {
    fn new() -> Self {
        Self { value: Arc::new(RwLock::new(HashMap::new())) }
    }
}

#[derive(Debug, Deserialize)]
struct Page {
    id: String
}

#[derive(Debug, Deserialize)]
struct Paste {
    content: String
}

#[async_std::main]
async fn main() -> tide::Result<()>{
    let mut app = tide::with_state(State::new());
    app.at("/").serve_file("static/index.html")?;
    app.at("/style.css").serve_file("static/style.css")?;
    app.at("/view").get(view);
    app.at("/create").post(create);
    app.listen("127.0.0.1:3000").await?;
    Ok(())
}

async fn view(req: Request<State>) -> tide::Result {
    let Page { id } = req.query()?;
    let response = match req.state().value.read().unwrap().get(&id) {
        Some(content) => Response::builder(200)
            .content_type("text/html")
            .body(format!("\
                <link rel=\"stylesheet\" href=\"/style.css\" />\
                <div class=\"container\">\
                    {}\
                </div>\
            ", content)).build(),
        None => Response::builder(404).build()
    };
    Ok(response)
}

async fn create(mut req: Request<State>) -> tide::Result {
    let Paste { content } = req.body_form().await?;
    let id = "abcdefghijklmnopqrstuvwxyz"
        .chars()
        .collect::<Vec<char>>()
        .choose_multiple(&mut rand::thread_rng(), 16)
        .collect::<String>();
    req.state().value.write().unwrap().insert(id.clone(), content);
    Ok(Redirect::new(format!("/view?id={}", id)).into())
}
