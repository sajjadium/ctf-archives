from flask import Flask, request, make_response
import jinja2
from jinja2 import PackageLoader
import random
import string
import json
import base64

app = Flask(__name__)

class Bidda:
  def __init__(self, name, population, image):
    self.name = name
    self.population = population
    self.image = image

  def __repr__(self):
    return self.name

random_string = ''.join(random.choice(string.ascii_letters) for i in range(10))
env = jinja2.Environment(loader=PackageLoader("app"),
                         block_start_string='@'+random_string,
                         block_end_string=random_string+'@',
                         variable_start_string='!'+random_string,
                         variable_end_string=random_string+'!')

default_biddas = [Bidda("Sardara", "3902", "https://www.borghiautenticiditalia.it/sites/default/files/Sardara_high.jpg"),
                  Bidda("Senorbi", "4778", "http://www.acrosstirreno.eu/sites/default/files/turismo/digital_183951_0.jpg"),
                  Bidda("Baradili", "75", "https://www.vistanet.it/cagliari/wp-content/uploads/sites/2/2017/11/FotoBaradiliComune08-770x480.jpg"),
                  Bidda("Borore", "1976", "https://www.sardegnaturismo.it/sites/default/files/galleria/005_borore_02_tomba_dei_giganti_imbertighe.jpg"),
		              Bidda("Domusnovas", "5869", "https://www.arketipomagazine.it/wp-content/uploads/sites/20/2020/04/SanGiovanni_011.jpg")]

for bidda in default_biddas:
  env.__dict__[bidda.name] = bidda

def prepareTemplates():
  for template in ["index.html", "inspect_bidda.html"]:
    with open("/home/templates/"+template, 'rb') as original:
      old_template = original.read()
    with open("/home/templates/"+template, 'wb') as modified:  
      new_template = old_template.replace(b"{{", b"!"+random_string.encode())
      new_template = new_template.replace(b"}}", random_string.encode()+b"!")
      new_template = new_template.replace(b"{%", b"@"+random_string.encode())
      new_template = new_template.replace(b"%}", random_string.encode()+b"@")
      modified.write(new_template)

@app.get("/")
def index():
	return env.get_template("index.html").render(env=env)

@app.route("/send_bidda", methods=["GET", "POST"])
def send_bidda():
  if request.method == "GET":
    return env.get_template("send_bidda.html").render()
  else:
    name = request.form.get("name")
    population = request.form.get("population")
    image = request.form.get("image")
    template = f"<h1> { name } </h1> <h2> { population } </h2> <img src=\"{ image }\" />"

    biddas = request.cookies.get("biddas")
    if biddas:
      biddas = json.loads(base64.b64decode(biddas))
      biddas.append({"name": name,"population" : population, "image" :image})
    else:
      biddas = [{"name": name,"population" : population, "image" :image}]
    resp = make_response(env.from_string(template).render())
    resp.set_cookie("biddas", base64.b64encode(json.dumps(biddas).encode()).decode())
    return resp

@app.get("/inspect_bidda")
def inspect_bidda():
  name = request.args.get("name")
  biddas = request.cookies.get("biddas")
  if biddas:
    biddas = json.loads(base64.b64decode(biddas))
    for bidda in biddas:
      if bidda["name"] == name:
        return env.get_template("inspect_bidda.html").render(env=env, bidda=bidda)
    return env.get_template("inspect_bidda.html").render(env=env, name=name)
  else:
    return env.get_template("send_bidda.html").render()

if __name__ == "__main__":
    prepareTemplates()
    app.run("0.0.0.0", port=5000)
