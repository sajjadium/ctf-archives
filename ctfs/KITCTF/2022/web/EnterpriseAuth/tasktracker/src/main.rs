mod template;

use axum::{
    http::{Request, StatusCode},
    extract::{Extension, Form},
    middleware::{self, Next},
    response::{IntoResponse, Redirect, Response, Html},
    routing::{get, post},
    Router,
};
use serde::Deserialize;
use std::collections::HashMap;
use std::net::SocketAddr;
use std::sync::{Arc, RwLock};
use std::env;

use crate::template::HtmlTemplate;
use crate::template::IndexTemplate;

const USER_HEADER: &str = "remote-user";

type SharedState = Arc<RwLock<AppState>>;

#[derive(Default)]
struct AppState {
    pub users: HashMap<String, Vec<String>>,
}

#[derive(Clone)]
struct CurrentUser {
    pub name: String,
}

async fn auth<B>(mut req: Request<B>, next: Next<B>) -> Result<Response, StatusCode> {
    let user_header = req
        .headers()
        .get(USER_HEADER)
        .and_then(|header| header.to_str().ok());

    match user_header {
        Some(name) => {
            println!("user: {} url: {}", &name, &req.uri());
            let user = CurrentUser { name: name.clone().to_string() };
            req.extensions_mut().insert(user);
            Ok(next.run(req).await)
        }
        _ => {
            println!("unauthorized url: {}", req.uri());
            Err(StatusCode::UNAUTHORIZED)
        },
    }
}

async fn list_tasks(
    Extension(state): Extension<SharedState>,
    Extension(user): Extension<CurrentUser>,
) -> impl IntoResponse {
    let users = &state.read().unwrap().users;

    let logs = match users.get(&user.name) {
        Some(user_logs) => user_logs.clone(),
        None => vec!["Add your first task".into()],
    };

    let template = IndexTemplate { logs };

    HtmlTemplate(template)
}

#[derive(Deserialize)]
struct NewTask {
    pub task: String,
}

async fn add_task(
    Extension(state): Extension<SharedState>,
    Extension(user): Extension<CurrentUser>,
    Form(form): Form<NewTask>
) -> impl IntoResponse {
    let users = &mut state.write().unwrap().users;

    println!("[adding task] user: {}, task: {}", &user.name, form.task);

    if users.contains_key(&user.name) {
        users.get_mut(&user.name).unwrap().push(form.task);
    } else {
        users.insert(user.name, vec![form.task]);
    }

    Redirect::to("/")
}

// TODO: add UI for this
// Currently waiting for design team
#[derive(Deserialize)]
struct ShareRequest {
    pub receiver: String,
}

async fn share_tasks(
    Extension(state): Extension<SharedState>,
    Extension(user): Extension<CurrentUser>,
    Form(form): Form<ShareRequest>
) -> impl IntoResponse {
    let users = &mut state.write().unwrap().users;

    println!("[share] from: {}, to: {}", &user.name, &form.receiver);

    if !users.contains_key(&form.receiver) || !users.contains_key(&user.name) {
        return Html("User not found");
    }

    let tasks = users.get(&user.name).unwrap().clone();

    users.get_mut(&form.receiver).unwrap()
        .extend_from_slice(&tasks);

    Html("Shared todolist with user")
}

#[tokio::main]
async fn main() {
    let shared_state = SharedState::default();

    {
        let users = &mut shared_state.write().unwrap().users;

        users.insert("admin".into(), vec![
            env::var("FLAG").unwrap_or("flag{test}".into())
        ]);
    }

    let app = Router::new()
        .route("/", get(list_tasks))
        .route("/", post(add_task))
        .route("/share", post(share_tasks))
        .route_layer(middleware::from_fn(auth))
        .layer(Extension(shared_state));

    let addr = SocketAddr::from(([0, 0, 0, 0], 3000));
    println!("listening on {}", addr);
    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}
