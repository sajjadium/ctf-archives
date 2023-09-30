#! /usr/bin/env python3

import os
from flask import Flask, request
from challenge import compute

app = Flask(__name__)

if not os.path.exists("./files"):
    os.mkdir("./files")

# Fixare path traversal
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() == "zip"


@app.route("/", methods=["GET", "POST"])
def upload_zip():
    alert = ''
    if request.method == "POST":
        if "file" not in request.files:
            return "No file"
        file = request.files["file"]
        if file.filename == "":
            return "No file"
        filename = os.urandom(16).hex()
        file.save(os.path.join("./files", filename + ".zip"))
        result =  compute(filename)
        alert = f"""
<div class="alert alert-primary" role="alert">
  <b id="result">{result}</b>
</div>
"""

    return f"""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ZIP Extractor 3000</title>

    <link
      rel="stylesheet"
      href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"
    />
  </head>
  <body>
    <div
      class="modal modal-sheet position-static d-block bg-body-secondary p-4 py-md-5"
      tabindex="-1"
      role="dialog"
      id="modalSheet"
    >
      <div class="modal-dialog" role="document">
        <form method="POST" enctype="multipart/form-data">
          <div class="modal-content rounded-4 shadow">
            <div class="modal-header border-bottom-0">
              <h1 class="modal-title fs-5">Upload your zip</h1>
            </div>
            <div class="modal-body py-0">
              {alert}
              <div class="form-group">
                <label for="file">Choose a file:</label>
                <input
                  type="file"
                  class="form-control-file"
                  id="file"
                  name="file"
                  accept=".zip"
                />
              </div>
            </div>
            <div
              class="modal-footer flex-column align-items-stretch w-100 gap-2 pb-3 border-top-0"
            >
              <button type="submit" class="btn btn-lg btn-primary">
                Upload
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
  </body>
</html>
"""
