use std::env;
use std::fs;
use std::io::Write;
use std::path;

const TOP_CODE: &str = r#"
import { crypto } from "https://deno.land/std@0.161.0/crypto/mod.ts";

const input = JSON.parse(Deno.args[0]);
const output: Record<string, unknown> = {};
"#;

const BOTTOM_CODE: &str = r#"
if ("{{FLAG}}" in output) {
  delete output["{{FLAG}}"];
}

const filename = crypto.randomUUID().replaceAll("-", "") + ".json";
await Deno.writeTextFile(filename, JSON.stringify(output));
console.log(filename);
"#;

fn get_program(user_src: &str) -> String {
    let flag = env::var("FLAG").unwrap();
    assert!(!flag.contains('"') && !flag.contains('\\'));

    [TOP_CODE, user_src, &BOTTOM_CODE.replace("{{FLAG}}", &flag)].join("\n")
}

fn get_preview(user_src: &str) -> String {
    [TOP_CODE, user_src, BOTTOM_CODE].join("\n")
}

pub fn generate(user_src: &str, user_id: &str) -> std::io::Result<String> {
    let user_path = path::Path::new("sandbox").join(user_id);
    fs::create_dir(&user_path)?;

    let program_path = user_path.join("main.ts");
    let preview_path = user_path.join("preview.ts");
    let program_src = get_program(user_src);
    let preview_src = get_preview(user_src);
    fs::File::create(&program_path)?.write_all(program_src.as_bytes())?;
    fs::File::create(&preview_path)?.write_all(preview_src.as_bytes())?;

    Ok(user_path.to_string_lossy().to_string())
}
