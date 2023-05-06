use reqwasm::http::Request;
use wasm_bindgen::JsValue;
use yew::prelude::*;

use crate::{APIResponse, APIStatus, Item, ShopItem};

#[function_component(Shop)]
pub fn shop() -> Html {
    let items = use_state(Vec::<ShopItem>::new);
    {
        let items = items.clone();
        use_effect_with_deps(
            move |_| {
                wasm_bindgen_futures::spawn_local(async move {
                    let resp: APIResponse = Request::get("/api/items")
                        .send()
                        .await
                        .unwrap()
                        .json()
                        .await
                        .unwrap();

                    if resp.status == APIStatus::Success {
                        items.set(
                            serde_json::from_value::<Vec<ShopItem>>(resp.data.unwrap()).unwrap(),
                        );
                    }
                });
                || ()
            },
            (),
        );
    }

    html! {
        <>
            <p class="title is-size-5">{"Shop:"}</p>
            <div class="columns">
                {
                    (*items).clone().into_iter().map(|item| html! {
                        <div class="card column m-3">
                            <div class="card-image">
                                <figure class="image">
                                    <img src={item.image.to_string()} style="width: 8rem; height: auto" alt="shop image" />
                                </figure>
                            </div>
                            <div class="content">
                                <p class="title is-4 mt-2">{item.name.to_string()}</p>
                                <p class="subtitle is-6">{"Price: "}{item.price}{" credits"}</p>
                                <button class="button is-primary" onclick={{
                                    let item = item.clone();
                                    Callback::from(move |_| {
                                        let item = item.clone();
                                        let window = web_sys::window().unwrap();
                                        let input = window.prompt_with_message_and_default(
                                            "How many?", "1"
                                        );
                                        let quantity_str = input.unwrap().unwrap_or_else(|| "0".to_string());

                                        let quantity = match quantity_str.parse::<i32>() {
                                            Ok(num) => num,
                                            Err(_) => {
                                                window.alert_with_message("Invalid quantity");
                                                return;
                                            }
                                        };

                                        if quantity <= 0 {
                                            return;
                                        }

                                        wasm_bindgen_futures::spawn_local(async move {
                                            let item = item.clone();
                                            let resp: APIResponse = Request::post("/api/buy")
                                                .header("Content-Type", "application/json")
                                                .body(JsValue::from_str(&serde_json::to_string(&Item {
                                                    name: item.name, quantity
                                                }).unwrap()))
                                                .send()
                                                .await
                                                .unwrap()
                                                .json()
                                                .await
                                                .unwrap();

                                            if resp.status == APIStatus::Success {
                                                let window = web_sys::window().unwrap();
                                                let location = window.location();
                                                location.reload();
                                            }
                                            else {
                                                window.alert_with_message(&resp.message.unwrap());
                                            }
                                        });
                                    })
                                }}>{"Buy"}</button>
                            </div>
                        </div>
                    }).collect::<Html>()
                }
            </div>
        </>
    }
}
