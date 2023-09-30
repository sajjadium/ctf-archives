from Borraccia import App, render_template, set_status_code

app = App(__name__)

def index(ctx):
    return render_template("index.html")

def documentation_test(ctx):
    return render_template("documentation_test.html")

def login(ctx):
    return render_template("login.html")

def register(ctx):
    return render_template("register.html")

def login_handle(ctx):
    data = ctx.request.post_data

    username = data.get("username")
    password = data.get("password")
    
    if username == "admin" and password == "admin":
        return render_template("login.html", status="Hi admin! Sorry, no flag for you!")
    
    set_status_code(ctx, 401)
    return render_template("login.html", status="Login failed")
    
def register_handle(ctx):
    data = ctx.request.post_data

    username = data.get("username")
    password = data.get("password")
    
    assert username and password
    
    return "Registered!"

app.get("/", index)
app.get("/index", index)
app.get("/login", login)
app.get("/register", register)
app.get("/documentation_test", documentation_test)

app.post("/login", login_handle)
app.post("/register", register_handle)


if __name__ == "__main__":
    app.run("0.0.0.0", 1337)
    
