import re
from flask import Flask, render_template, request, render_template_string

app = Flask(__name__)

s = {
    "austria-1": {
        "url": "https://cdn.discordapp.com/attachments/803887398105776168/872209040694972416/20210803_140556.jpg",
        "title": "The woods and fallen log in the Austrian Alps"
    },
    "austria-2": {
        "url": "https://cdn.discordapp.com/attachments/803887398105776168/872209041458343996/20210803_140551.jpg",
        "title": "Pretty scenery in the Austrian Alps 1"
    },
    "austria-3": {
        "url": "https://cdn.discordapp.com/attachments/803887398105776168/872209042179756082/20210803_110342.jpg",
        "title": "Pretty scenery in the Austrian Alps 2"
    },
    "munchen-1": {
        "url": "https://cdn.discordapp.com/attachments/803887398105776168/898209515353296896/20211014_123744.jpg",
        "title": "Early flying machines from the Deutsches Museum"
    },
    "munchen-2": {
        "url": "https://cdn.discordapp.com/attachments/803887398105776168/898212502024900619/20211014_161417.jpg",
        "title": "Street buildings of Munich"
    },
    "goethe": {
        "url": "https://cdn.discordapp.com/attachments/803887398105776168/999523569904140288/6d22649e-eaec-46d9-a788-e34c22421f5d.jpg",
        "title": "Manuscripts from the Goethe Gartenhaus"
    }
}

def check(string):
    blacklist = ["__init__", "__globals__", "nl", "subprocess", "config", "\\{\\{", "\\}\\}", "\\[", "\\]", " ", "update"]
    for word in blacklist:
        if re.search(word, string):
            return False
    return True

@app.route("/", methods=["POST", "GET"])
def home():
    cont = {}
    if request.method == "POST":
        if not "search" in request.form or not request.form["search"]:
            cont["status"] = "no_query"
            cont["images"] = s
            return render_template("index.html", context=cont)
            
        query = request.form["search"]
        
        if len(query) >= 68:
            cont["status"] = "over_limit"
            return render_template("index.html", context=cont)
        
        if not check(query):
            cont["status"] = "red_alert"
            return render_template("index.html", context=cont)

        for i in s:
            if re.search(f"{query}", s[i]["title"], flags=re.IGNORECASE):
                if not "images" in cont:
                    cont["images"] = {}
                cont["images"][i] = s[i]
                
        if not cont:
            cont["status"] = "not_found"
        else:
            cont["status"] = "found"
            cont["found"] = len(cont["images"])
            
        cont["query"] = query
        ret = render_template("index.html", context=cont)
        return render_template_string(ret)
        
    cont["status"] = "get"
    cont["images"] = s
    return render_template("index.html", context=cont)
    
if __name__ == "__main__":
    app.run("0.0.0.0", port=1337)
