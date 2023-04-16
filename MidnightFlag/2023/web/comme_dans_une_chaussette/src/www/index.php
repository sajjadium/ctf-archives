<!DOCTYPE HTML>
<head>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.7/dist/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <a class="navbar-brand" href="#">Parameter Sanitizer</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item active">
        <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
      </li>
  </div>
</nav>
<div class="container">
    <div class="row">
        <div class="col">
            <p class="lead">
                Welcome on "Parameter Sanitizer", a simple PHP application that shows you how a user input should be sanitized !
            </p>
            <p class="lead">
                You can check for XSS, SQLi, ... this is a beta test for the instance, but the final version of it with a API that sanitize will be release soon !
            </p>
            <hr/>
            <table class="table table-dark">
                <thead>
                    <tr>
                    <th scope="col">Vulnerability</th>
                    <th scope="col">Your Input</th>
                    <th scope="col">Send !</th>
                    <th scope="col">Result</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                    <th scope="row">XSS</th>
                    <td><input type="text" id="xss"></input></td>
                    <td><button class="btn btn-primary" onclick="send('xss')">Send</button></td>
                    <td id="res_xss"></td>
                    </tr>
                    <tr>
                    <th scope="row">SQL Injection</th>
                    <td><input type="text" id="sqli"></input></td>
                    <td><button class="btn btn-primary" onclick="send('sqli')">Send</button></td>
                    <td id="res_sqli"></td>
                    </tr>
                    <tr>
                    <th scope="row">Double encoding</th>
                    <td><input type="text" id="de"></input></td>
                    <td><button class="btn btn-primary" onclick="send('de')">Send</button></td>
                    <td id="res_de"></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</div>
<script>
function send(type)
{
    var data = {"type":type, "payload":btoa($(`#${type}`).val())}
    $(`#res_${type}`).empty()
    $.ajax({
        type: "POST",
        url: "/check.php",
        dataType: "json",
        data: JSON.stringify(data),
        success: function(msg)
        {
            if(msg["error"] != undefined)
            {
                alert(msg["error"])
            }
            else if(msg["ok"] != undefined)
            {
                data = atob(msg["ok"])
                $(`#res_${type}`).append(`<p>${data}</p>`)
            }
        }
    })
}
</script>
</body>
</html>