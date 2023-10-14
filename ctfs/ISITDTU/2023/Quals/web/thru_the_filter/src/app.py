from flask import Flask, request, render_template_string,redirect

app = Flask(__name__)
def check_payload(payload):
    blacklist = ['import', 'request', 'init', '_', 'b', 'lipsum', 'os', 'globals', 'popen', 'mro', 'cycler', 'joiner', 'u','x','g','args', 'get_flashed_messages', 'base', '[',']','builtins', 'namespace', 'self', 'url_for', 'getitem','.','eval','update','config','read','dict']
    for bl in blacklist:
        if bl in payload:
            return True
    return False
@app.route("/")
def home():
    if request.args.get('c'):
        ssti=request.args.get('c')
        if(check_payload(ssti)):
            return "HOLD UP !!!"
        else:
            return render_template_string(request.args.get('c'))
    else:
        return redirect("""/?c={{ 7*7 }}""")


if __name__ == "__main__":
    app.run()
