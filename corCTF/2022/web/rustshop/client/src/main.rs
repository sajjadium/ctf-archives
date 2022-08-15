use serde::{Deserialize, Serialize};
use yew::prelude::*;
use yew_router::prelude::*;

mod components;
mod routes;

#[derive(Clone, Routable, PartialEq)]
enum Route {
    #[at("/")]
    Home,
    #[at("/login")]
    Login,
    #[at("/register")]
    Register,
}

#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct Item {
    pub name: String,
    pub quantity: i32,
}

#[derive(Clone, Debug, Deserialize, PartialEq)]
pub struct ShopItem {
    pub name: String,
    pub image: String,
    pub price: i32,
}

#[derive(Clone, Debug, Deserialize, PartialEq)]
pub struct User {
    pub username: String,
    pub password: String,
    pub money: i32,
    pub items: Vec<Item>,
}

#[derive(Clone, Debug, PartialEq)]
pub struct UserContext {
    pub logged_in: bool,
    pub user: Option<User>,
}

#[derive(Debug, Deserialize, PartialEq)]
#[serde(rename_all = "lowercase")]
pub enum APIStatus {
    Success,
    Error,
}

#[derive(Debug, Deserialize)]
pub struct APIResponse {
    pub status: APIStatus,
    pub data: Option<serde_json::Value>,
    pub message: Option<String>,
}

fn switch(routes: &Route) -> Html {
    match routes {
        Route::Home => html! { <routes::home::Home /> },
        Route::Login => html! { <routes::login::Login /> },
        Route::Register => html! { <routes::register::Register /> },
    }
}

#[function_component(Main)]
fn app() -> Html {
    html! {
        <BrowserRouter>
            <Switch<Route> render={Switch::render(switch)} />
        </BrowserRouter>
    }
}

fn main() {
    wasm_logger::init(wasm_logger::Config::default());
    yew::start_app::<Main>();
}
