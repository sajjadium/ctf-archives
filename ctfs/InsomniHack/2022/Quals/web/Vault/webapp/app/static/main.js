
function loadPage() {
    var pages = document.getElementsByClassName("page");
    for(var i = 0; i < pages.length; i++) {
        pages[i].style.display = 'none';
    }
    $.query.parseNew(location.hash);
    switch($.query.get("page")) {
        case "secrets":
            var secrets_element = document.getElementById('secrets').childNodes[3];
            
            document.getElementById("secrets").style.display = 'block';
            var secrets;
            $.get("api/secrets", function(data) {
                secrets = data.result;
                secrets_element.innerHTML = '';
                secrets.forEach(secret =>  {
                    var sec = document.createElement("div");
                    sec.setAttribute("class","secret");
                    var el = document.createElement("div");
                    el.setAttribute("class","secret_name");
                    el.innerText = secret.secret_name;
                    var el2 = document.createElement("div");
                    el2.setAttribute("class","secret_value");
                    el2.innerText = secret.secret_value;
                    sec.appendChild(el);
                    sec.appendChild(el2);
                    secrets_element.appendChild(sec);
                });
                
                
            }, "json");
            break;
        case "home":
            document.getElementById('home').style.display = 'block';
            break;
        case "login":
            document.getElementById('login').style.display = 'block';
            break;
        case "logout":
            $.get("api/logout", function(e) {
                window.location.hash = "page=home";
                location.reload();
            });
            break;
        case "report":
            document.getElementById('report').style.display = 'block';
            break;
        case "register":
            document.getElementById('register').style.display = 'block';
            break;
        default:
            break;
    }
}

function secret() {
    $.post("api/secrets", $("#secretform").serialize(), function(e) {
        if(e.status != "OK") {
            showError(e.msg);
        }
        else {
            location.reload();
        }
    },"json");
}

function login() {
    $.post("api/login", $("#loginform").serialize(), function(e) {
        if(e.status != "OK") {
            showError(e.msg);
        }
        else {
            window.location.hash = "page=secrets";
            location.reload();
        }
    },"json");
}

function register() {
    $.post("api/register", $("#registerform").serialize(), function(e) {
        if(e.status != "OK") {
            showError(e.msg);
        }
        else {
            window.location.hash = "page=login";
        }
    },"json");
}

function report() {
    $.post("api/report", $("#reportform").serialize(), function(e) {
        if(e.status != "OK") {
            showError(e.msg);
        }
        else {
            window.location.hash = "page=home";
        }
    },"json");
}

$(window).bind('load', function(e) {
    if(window.location.hash.length == 0) {
        window.location.hash = "#page=home";
    }
    loadPage();
});
$(window).bind( 'hashchange', function(e) {
    loadPage();
});

function showError(e) {
    $("#error")[0].innerHTML = e;
    $("#error")[0].style.display = 'block';
}
function closeError() {
    $("#error")[0].innerHTML = '';
    $("#error")[0].style.display = 'none';
}