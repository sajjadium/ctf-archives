use yew::prelude::*;

#[function_component(Hero)]
pub fn hero() -> Html {
    html! {
        <section class="hero is-info section">
            <div class="container">
                <p class="title has-text-weight-bold">
                    {"🦀 rustshop 🦀"}
                </p>
                <p class="subtitle">
                    {"the only shop containing everything a rust user needs!"}
                </p>
            </div>
        </section>
    }
}
