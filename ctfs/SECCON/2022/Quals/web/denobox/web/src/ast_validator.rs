use deno_ast::swc::ast::{
    AssignExpr, BinExpr, BlockStmt, Expr, ExprStmt, Ident, Lit, MemberExpr, MemberProp, ModuleItem,
    Pat, Stmt, UnaryExpr,
};

fn validate_identifier(ident: &Ident) -> Result<(), String> {
    // Limit available variables to `input` and `output` only.
    if ident.sym.eq("input") || ident.sym.eq("output") {
        Ok(())
    } else {
        Err(format!("{:?}", ident))
    }
}

fn validate_unary_expr(expr: &UnaryExpr) -> Result<(), String> {
    validate_expr(&expr.arg)
}

fn validate_binary_expr(expr: &BinExpr) -> Result<(), String> {
    validate_expr(&expr.left)?;
    validate_expr(&expr.right)?;
    Ok(())
}

fn validate_assign_expr(expr: &AssignExpr) -> Result<(), String> {
    (match expr.left.as_pat() {
        Some(Pat::Expr(expr)) => validate_expr(expr),
        _ => Err(format!("{:?}", expr.left)),
    })?;
    validate_expr(&expr.right)?;
    Ok(())
}

fn validate_member_expr(expr: &MemberExpr) -> Result<(), String> {
    validate_expr(&expr.obj)?;
    (match &expr.prop {
        MemberProp::Ident(_) => Ok(()),
        _ => Err(format!("{:?}", expr.prop)),
    })?;
    Ok(())
}

fn validate_literal(lit: &Lit) -> Result<(), String> {
    match lit {
        Lit::Str(_) | Lit::Bool(_) | Lit::Null(_) | Lit::Num(_) => Ok(()),
        _ => Err(format!("{:?}", lit)),
    }
}

fn validate_expr(expr: &Expr) -> Result<(), String> {
    // ref. https://rustdoc.swc.rs/swc_ecma_ast/enum.Expr.html
    match expr {
        Expr::Unary(expr) => validate_unary_expr(expr),
        Expr::Bin(expr) => validate_binary_expr(expr),
        Expr::Assign(expr) => validate_assign_expr(expr),
        Expr::Member(expr) => validate_member_expr(expr),
        Expr::Ident(ident) => validate_identifier(ident),
        Expr::Lit(lit) => validate_literal(lit),
        _ => Err(format!("{:?}", expr)),
    }
}

fn validate_stmt(stmt: &Stmt) -> Result<(), String> {
    // ref. https://rustdoc.swc.rs/swc_ecma_ast/enum.Stmt.html
    match stmt {
        Stmt::Block(BlockStmt { span: _, stmts }) => stmts.iter().try_for_each(validate_stmt),
        Stmt::Empty(_) => Ok(()),
        Stmt::Expr(ExprStmt { span: _, expr }) => validate_expr(expr),
        _ => Err(format!("{:?}", stmt)),
    }
}

pub fn validate(source: &str) -> Result<&str, String> {
    let text_info = deno_ast::SourceTextInfo::new(source.into());

    let parsed_source = deno_ast::parse_module(deno_ast::ParseParams {
        specifier: String::from("file:///main.ts"),
        text_info,
        media_type: deno_ast::MediaType::TypeScript,
        capture_tokens: true,
        scope_analysis: false,
        maybe_syntax: None,
    })
    .map_err(|info| format!("Parse error: {}", info.message()))?;

    let module = parsed_source.module();

    if module.shebang.is_some() {
        Err("Do not use shebang")?;
    }
    for item in module.body.iter() {
        (match item {
            ModuleItem::Stmt(stmt) => validate_stmt(stmt),
            _ => Err(format!("{:?}", item)),
        })
        .map_err(|node| format!("Parse error at {:?}", node))?;
    }

    Ok(source)
}
