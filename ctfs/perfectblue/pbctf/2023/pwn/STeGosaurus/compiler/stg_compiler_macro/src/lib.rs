use proc_macro::TokenStream;

#[proc_macro]
pub fn stg(tok: TokenStream) -> TokenStream {
    let module = syn::parse_macro_input!(tok as stg_compiler::compile::Module);
    match module.compile() {
        Ok(res) => {
            let data = bincode::serialize(&res)
                .unwrap();
            quote::quote!([#(#data),*])
        },
        Err(res) => return res.to_compile_error().into(),
    }.into()
}
