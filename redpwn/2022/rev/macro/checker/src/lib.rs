use proc_macro::TokenStream;
use proc_macro2::Span;
use syn::ItemMod;

#[macro_use]
extern crate quote;
#[macro_use]
extern crate syn;


fn dicerator(v: &ItemMod) -> syn::Expr {
    match v.ident.to_string().as_ref() {
        "a" => {
            syn::Expr::Paren(syn::ExprParen {
                attrs: Vec::new(),
                paren_token: syn::token::Paren { span: Span::call_site() },
                expr: v.content.as_ref().unwrap().1.iter()
                    .fold(
                        Box::new(syn::Expr::Verbatim(quote! { 0 })),
                        |a,b| {
                            Box::new(syn::Expr::Binary(syn::ExprBinary {
                                attrs: Vec::new(),
                                left: a,
                                op: syn::BinOp::Add(syn::token::Add(Span::call_site())),
                                right: match b {
                                    syn::Item::Mod(x) => Box::new(dicerator(x)),
                                    _ => panic!("wrong")
                                },
                            }))
                        }
                    )
            })
        }
        "m" => {
            syn::Expr::Paren(syn::ExprParen {
                attrs: Vec::new(),
                paren_token: syn::token::Paren { span: Span::call_site() },
                expr: v.content.as_ref().unwrap().1.iter()
                    .fold(
                        Box::new(syn::Expr::Verbatim(quote! { 1 })),
                        |a,b| {
                            Box::new(syn::Expr::Binary(syn::ExprBinary {
                                attrs: Vec::new(),
                                left: a,
                                op: syn::BinOp::Mul(syn::token::Star(Span::call_site())),
                                right: match b {
                                    syn::Item::Mod(x) => Box::new(dicerator(x)),
                                    _ => panic!("wrong")
                                },
                            }))
                        }
                    )
            })
        }
        "o" => {
            syn::Expr::Verbatim(quote! { 1 })
        }
        _ => { panic!("wrong") }
    }
}


#[proc_macro_attribute]
pub fn check_flag(_: TokenStream, item: TokenStream) -> TokenStream {    
    let ast = parse_macro_input!(item as syn::ItemMod);

    let name = ast.ident;
    let mut parts = quote!();

    let (_, items) = ast.content.unwrap();
    assert!(items.len() <= 32, "wrong");

    for item in items {
        match item {
            syn::Item::Mod(base) => {
                let v = dicerator(&base);
                parts.extend(quote! {
                    let a = (a + (q * #v)) % 4294967291;
                    let q = (q * v) % 4294967291;
                });
            }
            _ => panic!("wrong")
        }
    }

    quote! {
        mod #name {
            pub fn dice(v: u32) -> u32 {
                let v = v as u64;
                let q = 1 as u64;
                let a = 0u64;
                #parts
                a as u32
            }

            pub fn verify(a: &[u32], b: &[u32]) -> bool {
                for i in 0..a.len() {
                    if dice(a[i]) != b[i] {
                        return false;
                    }
                }
                true
            }

            pub fn flag(a: &[u32]) -> String {
                String::from_utf8(
                    a.iter()
                        .map(|x| dice(*x))
                        .filter(|x| 0x20 <= *x && *x <= 0x7f)
                        .map(|x| x as u8)
                        .collect()
                ).unwrap()
            }
        }
    }.into()
}
