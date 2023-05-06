import shutil
from bs4 import BeautifulSoup
import os
import random
import time
import tempfile
from flask import Flask, request, render_template, session, jsonify
from werkzeug.utils import secure_filename
import requests


app = Flask(__name__)

rust_template = """
#![allow(warnings, unused)]
use std::collections::HashMap;
use std::fs;
use std::env;
extern crate seccomp;
extern crate libc;

extern crate tiny_http;
extern crate seccomp_sys;
use seccomp::*;

use tiny_http::{Server, Response, Header, Request};

static ALLOWED: &'static [usize] = &[0, 1, 3, 11, 44,
                                     60, 89, 131, 202,
                                     231, 318];

fn main() {
    let mut dir = env::current_exe().unwrap();
    dir.pop();
    dir.push("../../app.htmlrs");
    let template = fs::read_to_string(dir.to_str().unwrap()).unwrap();
    let server = Server::http("127.0.0.1:%s").unwrap();
    apply_seccomp();
    for request in server.incoming_requests() {
        println!("received request! method: {:?}, url: {:?}",
            request.method(),
            request.url(),
        );
        handle_request(request, &template);
        std::process::exit(0);
    }
}

fn handle_request(req: Request, template: &String) {
    let mut methods: HashMap<_, fn() -> String> = HashMap::new();
    %s
    let mut html = template.clone();
    for (name, fun) in methods.iter() {
        html = html.replace(name, &fun());
    }
    let header = Header::from_bytes(
        &b"Content-Type"[..], &b"text/html"[..]
    ).unwrap();
    let mut response = Response::from_string(html);
    response.add_header(header);
    req.respond(response).unwrap();
}

fn apply_seccomp() {
    let mut ctx = Context::default(Action::KillProcess).unwrap();
    for i in ALLOWED {
        let rule = Rule::new(*i, None, Action::Allow);
        ctx.add_rule(rule).unwrap();
    }
    ctx.load();
}
%s
"""

templ_fun = """
fn temp%s() -> String {
    %s
}
"""


def get_result(template_path: str):
    with open(template_path) as f:
        templ = f.read()

    with tempfile.TemporaryDirectory() as tmpdir:
        shutil.copytree('skeleton', tmpdir, dirs_exist_ok=True)
        os.chdir(tmpdir)
        port = str(random.randrange(40000, 50000))
        with open('src/main.rs', 'w') as f:
            soup = BeautifulSoup(templ, 'html.parser')
            funcs = []
            for i, temp in enumerate(soup.find_all('templ')):
                funcs.append(templ_fun % (i, temp.text))
                templ = templ.replace(f'<templ>{temp.text}</templ>', f'temp{i}', 1)
            hashmap = ""
            for i in range(len(funcs)):
                hashmap += f"""methods.insert("temp{i}", temp{i});\n"""
            f.write(rust_template % (port, hashmap, '\n'.join(funcs)))

        with open('app.htmlrs', 'w') as f:
            f.write(templ)

        os.system('cargo run --offline -q &')
        for _ in range(10):
            time.sleep(1)
            try:
                r = requests.get(f'http://localhost:{port}')
                os.chdir('/app')
                return r.text
            except:
                pass
        return "App failed to start"

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if not session.get('verified'):
        return "Please complete <pre>/pow</pre>", 403

    os.chdir('/app')
    if request.method == 'POST':
        try:
            file = request.files['file']
            path = os.path.join('uploads', secure_filename(file.filename))
            file.save(path)
            response = get_result(path)
            os.remove(path)
        except:
            return "There was an error"
        del session['verified']
        return render_template('upload.html', response=response)
    else:
        return render_template('upload.html')


@app.route("/pow", methods=["GET", "POST"])
def do_pow():
    if request.method == 'GET':
        import pow
        pref, suff = pow.generate()
        session['pref'], session['suff'], session['end'] = pref, suff, time.time() + 30
        time.sleep(1)
        return jsonify({"pref": pref, "suff": suff})
    else:
        import pow
        difficulty = int(os.getenv("DIFFICULTY", "6"))
        pref, suff = session['pref'], session['suff']
        answer = request.json.get('answer')
        if pow.verify(pref, suff, answer, difficulty):
            session['verified'] = True
            return "Thank you!"
        else:
            return "POW incorrect"

@app.before_request
def clear_cookies():
    # Prevent replay attack
    if session.get('end') and session['end'] < time.time():
        del session['pref']
        del session['suff']
        del session['end']

def load_app(key):
    app.secret_key = key
    return app
