<?php

function do_calcs($csv){
  preg_match_all("/{{([^}]*)}}/", $csv, $matches);
  
  foreach ($matches[1] as &$val){
    $csv = str_replace("{{" . $val . "}}", eval("return " . $val . ";"), $csv);
  }

  return $csv;
}

/* main */
if ($_SERVER['REQUEST_METHOD'] == "POST"){
  if (isset($_POST['csv'])){
    // do the math calculations
    $csv = trim(do_calcs($_POST['csv']));
    $csv = str_replace("\r\n", "\n", $csv); // replace CRLF to LF

    $result = csv_parse($csv);
    print_r($result);
  }
  else{
    die("Missing param csv");
  }
}

?>

<html>
<head>
<style>
@import url(https://fonts.googleapis.com/css?family=Roboto:300);

.login-page {
  width: 35%;
  padding: 3% 0 0;
  margin: auto;
}
.form {
  position: relative;
  z-index: 1;
  background: #FFFFFF;
  max-width: 100%;
  margin: 0 auto 40px;
  padding: 30px;
  text-align: center;
  box-shadow: 0 0 20px 0 rgba(0, 0, 0, 0.2), 0 5px 5px 0 rgba(0, 0, 0, 0.24);
}
.form #input {
  font-family: "Roboto", sans-serif;
  height: 30%;
  width: 100%;
  text-align: top;
  outline: 0;
  background: #f2f2f2;
  border: 0;
  margin: 0 0 15px;
  padding: 15px;
  box-sizing: border-box;
  font-size: 14px;
}
.form button {
  font-family: "Roboto", sans-serif;
  text-transform: uppercase;
  outline: 0;
  background: #4CAF50;
  width: 100%;
  border: 0;
  padding: 15px;
  color: #FFFFFF;
  font-size: 14px;
  -webkit-transition: all 0.3 ease;
  transition: all 0.3 ease;
  cursor: pointer;
}
.form button:hover,.form button:active,.form button:focus {
  background: #43A047;
}
.form .message {
  margin: 15px 0 0;
  color: #b3b3b3;
  font-size: 12px;
}
.form .message a {
  color: #4CAF50;
  text-decoration: none;
}
.form .register-form {
  display: none;
}
.container {
  position: relative;
  z-index: 1;
  max-width: 300px;
  margin: 0 auto;
}
.container:before, .container:after {
  content: "";
  display: block;
  clear: both;
}
.container .info {
  margin: 0px auto;
  text-align: center;
}
.container .info h1 {
  margin: 0 0 15px;
  padding: 0;
  font-size: 36px;
  font-weight: 300;
  color: #1a1a1a;
}
.container .info span {
  color: #4d4d4d;
  font-size: 12px;
}
.container .info span a {
  color: #000000;
  text-decoration: none;
}
.container .info span .fa {
  color: #EF3B3A;
}
body {
  overflow-y: hidden;
  background: #76b852; /* fallback for old browsers */
  background: -webkit-linear-gradient(right, #76b852, #8DC26F);
  background: -moz-linear-gradient(right, #76b852, #8DC26F);
  background: -o-linear-gradient(right, #76b852, #8DC26F);
  background: linear-gradient(to left, #76b852, #8DC26F);
  font-family: "Roboto", sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;      
}

#title {
  margin: 40px auto 0 auto;
  color: white;
}

.center{
  text-align: center;
}

</style>
</head>
<body>
<h1 id="title" class="center"> Secure and Fast PHP CSV Parser </h1>
<div class="login-page">
  <div class="form">
  <h3 class="center" style="font-size: 16px;">Try my CSV parser! The first line should contain keys and the other lines the data.You can also insert math operations inside your CSV data and my incredible parser will calculate it! Example: </h3>
  <h4 style="text-align: left; color: #4CAF50">price,tax<br>200,{{0.1*200}}</h4>
  <form class="login-form" method="POST">
      <textarea name="csv" id=input type="text" placeholder="CSV"></textarea>
      <button>Submit</button>
  </div>
</div>
</body>
</html>
