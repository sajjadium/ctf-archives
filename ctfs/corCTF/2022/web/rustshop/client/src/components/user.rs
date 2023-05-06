use yew::prelude::*;

use crate::User as BaseUser;

#[derive(Properties, PartialEq)]
pub struct UserProps {
    pub user: BaseUser,
}

#[function_component(User)]
pub fn user(props: &UserProps) -> Html {
    html! {
        <>
            <p class="title is-size-3">{"Hello, "}{props.user.username.to_string()}{"!"}</p>
            <p class="title is-size-5 mb-0">{"Money: "}{props.user.money}{" credits"}</p>
            <p class="title is-size-5 mt-1 mb-0">{"Items: "}</p>
            {
                props.user.items.clone().into_iter().map(|item| html! {
                    <p class="is-size-6">{item.name}{" - "}{item.quantity}{"x"}</p>
                }).collect::<Html>()
            }
        </>
    }
}
