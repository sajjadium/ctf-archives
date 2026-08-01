import os
from flask import *
from werkzeug.utils import secure_filename
from urllib.parse import unquote

UPLOAD_FOLDER = "shared_files/"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SHARED_FOLDER = os.path.join(BASE_DIR, "shared_files")

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = os.urandom(32)

@app.route('/')
def index():
    #Return the submission template
    return make_response(render_template("index.html"))

@app.post("/upload")
def upload():
    file = request.files["image"]
    filename = secure_filename(file.filename)
    
    #Check if file is a png
    if not filename.endswith('.png'):
        return "Invalid" + filename, 404
    
    file.save(UPLOAD_FOLDER + filename)
    response = make_response("Your image has successfully been uploaded to /files", 200)
    
    return response


@app.route('/files')
def list_files():
    #Get url parameters
    target_file = request.args.get('file')
    key = request.args.get('key')
    
    #Check for download request    
    if target_file:
        #Check for valid png file request
        if not target_file.lower().endswith('.png'):
            abort(403, description="Access denied. Only PNG images can be downloaded.")
        if '\x00' in target_file:
            abort(403, description="Access denied. Invalid Request.")
 
        #Process file path    
        target_file = unquote(target_file)
        target_file = target_file.split(chr(0))[0]
        file_path = os.path.join(SHARED_FOLDER, target_file)
        
        #Compute authentication value
        try:
            with open(file_path, 'rb') as f:
                secret_value = f.read(5).hex(' ').upper()
        except FileNotFoundError:
            abort(404)            
        
        #Check for valid key authentication
        if not key == secret_value:
            abort(403, description="Access denied. URL Downloading is only allowed with key authentication.")

        #Downloads the file to the user.        
        return send_from_directory(
            directory=SHARED_FOLDER, path=target_file, as_attachment=True)
 
    #Return a list of all files in directory if no download request.
    try:
        all_items = os.listdir(SHARED_FOLDER)
        files = [f for f in all_items if os.path.isfile(os.path.join(SHARED_FOLDER, f))]
        
        return render_template("files.html", files = files)
    except FileNotFoundError:
        return "Shared folder directory does not exist.", 500
    

@app.route('/files/<path:filename>')
def host_file(filename):
    #Check if the requested file is a png
    if not filename.lower().endswith('.png'):
            abort(403, description="Access denied. Only PNG images can be accessed.")
    
    #Return the requested file.        
    try:
        return send_from_directory(
            directory=SHARED_FOLDER, 
            path=filename,
            as_attachment=False  
        )
    except FileNotFoundError:
        abort(404)
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9972)
