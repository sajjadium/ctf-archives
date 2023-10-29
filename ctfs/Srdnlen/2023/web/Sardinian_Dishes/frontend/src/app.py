from flask import Flask, make_response, request
import pyratemp
import requests

app = Flask(__name__)

dishes = {
          'malloreddus':'Malloreddus, sometimes Italianized as gnocchetti sardi, are a type of pasta typical of Sardinian cuisine.',
          'seadas':'Seada is a Sardinian dessert. It is prepared by deep-frying a large semolina dumpling (usually between 8 and 10 cm in diameter) with a filling of soured Pecorino cheese and lemon peel',
          'carasau bread': 'Pane carasau is a traditional flatbread from Sardinia. It is called carta da musica in Italian, meaning "sheet music"',
          'casu marzu' : 'Casu Marzu is a traditional Sardinian sheep milk cheese that contains live insect larvae.',
          }

@app.get("/")
def index():
  template = pyratemp.Template(filename="/home/templates/index.html")
  return template(dishes=dishes)

@app.route('/recipe')
def get_product():
  name = request.args.get('name')
  if name == "casu marzu":
    resp = make_response("Forbidden - CASU MARZU IS ILLEGAL, YOU CAN'T COOK IT!")
    resp.status_code = 403
    return resp
  else:
    res = requests.get(f"http://web-dish-backend:5000/recipe?name={name}")
    template = pyratemp.Template(f"The recipe for {name} is at @! res.text !@")
    return template(res=res)
     


@app.route("/suggest", methods=["GET", "POST"])
def suggest():
  if request.method == "GET":
    template = pyratemp.Template(filename="/home/templates/suggest.html")
    return template()
  else:
    template = pyratemp.Template(f"{request.form['name']} - {request.form['description']}")
    return template()  


if __name__ == "__main__":
    app.run("0.0.0.0")
