use reqwasm::http::Request;
use yew::prelude::*;
use yew_router::prelude::*;

use crate::components::{hero, navbar, shop, user};
use crate::{APIResponse, APIStatus, Route, User, UserContext};

#[function_component(Home)]
pub fn home() -> Html {
    let user = use_state(|| UserContext {
        logged_in: false,
        user: None,
    });

    {
        let user = user.clone();
        use_effect_with_deps(
            move |_| {
                wasm_bindgen_futures::spawn_local(async move {
                    let resp: APIResponse = Request::get("/api/user")
                        .send()
                        .await
                        .unwrap()
                        .json()
                        .await
                        .unwrap();

                    if resp.status == APIStatus::Success {
                        user.set(UserContext {
                            logged_in: true,
                            user: Some(serde_json::from_value::<User>(resp.data.unwrap()).unwrap()),
                        });
                    } else {
                        user.set(UserContext {
                            logged_in: false,
                            user: None,
                        });
                    }
                });
                || ()
            },
            (),
        );
    }

    html! {
        <ContextProvider<UserContext> context={(*user).clone()}>
            <navbar::Navbar />
            <hero::Hero />
            if user.logged_in {
                <section class="section">
                    <div class="container">
                        <user::User user={(*user).clone().user.unwrap()} />
                        <hr />
                        <shop::Shop />
                    </div>
                </section>
            }
            else {
                <section class="section">
                    <div class="container is-flex is-flex-direction-column is-align-items-center">
                        <p class="is-size-4">{"Welcome to "}<strong>{"🦀 rustshop 🦀"}</strong>{"!"}</p>
                        <br />
                        <p class="is-size-6">{"To start buying items on "}<strong>{"🦀 rustshop 🦀"}</strong>{", you need to register or login."}</p>
                        <br />
                        <div class="buttons">
                            <Link<Route> to={Route::Register} classes="mx-1"><button class="button is-primary">{"Register"}</button></Link<Route>>
                            <Link<Route> to={Route::Login} classes="mx-1"><button class="button is-link">{"Login"}</button></Link<Route>>
                        </div>
                    </div>
                </section>
            }
        </ContextProvider<UserContext>>
    }
}
