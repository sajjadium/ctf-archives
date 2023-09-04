from flask import Flask, request, render_template
from utils import decrypt

app = Flask(
    __name__,
    static_url_path='/',
    static_folder='static/'
)

@app.route('/', methods=['GET'])
def index():
    if not "key" in request.args:
        return render_template('index.html')
    
    key_hex = request.args.get('key', None)
    if key_hex is None:
        return render_template('index.html')
    
    try:
        msg = decrypt(key_hex)
    except:
        msg = 'Something goofed up'
        
    return render_template('index.html', msg=msg)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)