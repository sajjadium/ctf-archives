from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from getExcelMetadata import getMetadata, extractWorkbook, findInternalFilepath, WORKBOOK
import shutil
import os
import uuid

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024

@app.errorhandler(413)
def filesize_error(e):
    return render_template("error_filesize.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/downloads/fizzbuzz")
def return_fizzbuzz():
    return send_file("./fizzbuzz.xlsm")

@app.route("/upload/testPandasImplementation")
def upload_file():
    return render_template("upload.html")
	
@app.route("/metadata", methods = ['GET', 'POST'])
def view_metadata():
    if request.method == "GET":
        return render_template("error_upload.html")

    if request.method == "POST":
        f = request.files["file"]
        
        tmpFolder = "./uploads/" + str(uuid.uuid4())
        os.mkdir(tmpFolder)
        filename = tmpFolder + "/" + secure_filename(f.filename)
        f.save(filename)

        try:
            properties = getMetadata(filename)
            extractWorkbook(filename, tmpFolder)
            workbook = tmpFolder + "/" + WORKBOOK
            properties.append(findInternalFilepath(workbook))
        except Exception:
            return render_template("error_upload.html")
        finally:
            shutil.rmtree(tmpFolder)
        
        return render_template("metadata.html", items=properties)
		
if __name__ == "__main__":
    app.run(host="0.0.0.0")