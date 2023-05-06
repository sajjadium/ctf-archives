from flask import *
app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def base():
    person = ""
    if request.method == 'POST':
      if request.form['name']:
        person = request.form['name']
    palte = '''
    <!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Secure Search</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
  </head>
  <body>
    <h1 class="container my-3">Hi, %s</h1>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-pprn3073KE6tl6bjs2QrFaJGz5/SUsLqktiwsUTF55Jfv3qYSDhgCecCxMW52nD2" crossorigin="anonymous"></script>
    <div class="container my-3">
        <form action="/" method="post">
            <div class="mb-3">
              <label for="text" class="form-label">Type your name here:- </label>
              <input type="text" class="form-control" name="name" id="text" value="">
            </div>
            <button type="submit" class="btn btn-primary">See magic</button>
          </form>
    </div>
</body>
</html>'''% person
    return render_template_string(palte)

if __name__=="__main__":
	app.run("0.0.0.0",port=5000,debug=False)