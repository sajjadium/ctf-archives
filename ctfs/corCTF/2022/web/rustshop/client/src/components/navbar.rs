use wasm_bindgen::JsCast;
use yew::prelude::*;
use yew_router::prelude::*;

use crate::{Route, UserContext};

#[function_component(Navbar)]
pub fn navbar() -> Html {
    let user = use_context::<UserContext>().unwrap_or(UserContext {
        logged_in: false,
        user: None,
    });

    let logout_onclick = {
        Callback::from(move |_| {
            let window = web_sys::window().unwrap();
            let document = window.document().unwrap();
            let html_document = document.dyn_into::<web_sys::HtmlDocument>().unwrap();
            html_document.set_cookie("session=; path=/api; max-age=0");
            let location = window.location();
            location.reload();
        })
    };

    html! {
        <nav class="container navbar">
            <div class="navbar-brand">
                <Link<Route> to={Route::Home} classes="navbar-item">
                    <h1 class="is-size-5 has-text-weight-bold">{"🦀 rustshop 🦀"}</h1>
                </Link<Route>>
            </div>
            <div class="navbar-menu is-active">
                <div class="navbar-end">
                    <div class="navbar-item">
                        if user.logged_in {
                            <button class="button is-primary" onclick={logout_onclick}>{"Logout"}</button>
                        }
                    </div>
                </div>
            </div>
        </nav>
    }
}
