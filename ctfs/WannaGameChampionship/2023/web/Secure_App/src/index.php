<?php

require_once 'config.php';

session_start();

if (@$_SESSION["isLoggedIn"]) {

  if ($_SESSION["username"] !== "admin") {
    $home_message_1 = "Welcome back hackers! This app was created by me to save the flag of mine 😉. And only if you are so nice to me, can i share it with you. Or ... just find another way to get the flag without my approval 😜.";
    $home_message_2 = "Good luck guy :v";
  } else {
    $home_message_1 = "Welcome back admin! ";
    $home_message_2 = "Good to see you <3 ";
  }

  $html = <<<EOF
<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>App - CTF</title>

    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.6.3/css/all.css" integrity="sha384-UHRtZLI+pbxtHCWp1t77Bi1L4ZtiqrqD80Kn4Z8NTSRyMA2Fd33n5dQ8lWUE00s/" crossorigin="anonymous">
    
    <link rel="stylesheet" href="assets/css/bootstrap4-neon-glow.min.css">
    <link rel="stylesheet" href="assets/css/main.css">
    <link rel="stylesheet" href="assets/css/particles.css">
    
    <link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">
    <link rel='stylesheet' href='https://cdn.jsdelivr.net/font-hack/2.020/css/hack.min.css'>
    
  </head>
  <body>

  <div id="particles-js"></div>
    <div class="navbar-dark text-white">
      <div class="container">
        <nav class="navbar px-0 navbar-expand-lg navbar-dark">
          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
            <div class="navbar-nav">
                <a href="index.php" class="pl-md-0 p-3 text-light">Home</a>
                <a href="admin.php" class="p-3 text-decoration-none text-light">Admin pannel</a>
                <a href="/api/logout.php" class="p-3 text-decoration-none text-light active">Logout</a>
          
            </div>
          </div>
        </nav>
  
      </div>
    </div>
    <div class="jumbotron bg-transparent mb-0 radius-0">
      <div class="container">
          <div class="row">
            <div class="col-xl-6">
              <h1 class="display-3">CAPTURE THE FLAG<span class="vim-caret">͏͏&nbsp;</span></h1>
              <div class="lead mb-3 text-mono text-success">$home_message_1
              </div>
              <div class="text-mono">
              <!--
                <a href="login.php"
                  title="Download Theme"
                  class="btn btn-success btn-shadow px-3 my-2 ml-0 text-left">
                  Login
                </a>
                <a href="registration.php"
                  class="btn btn-danger btn-shadow px-3 my-2 ml-0 ml-sm-1 text-left">
                  Register
                </a>
                -->
              </div>

              <div class="text-darkgrey text-mono my-2"> $home_message_2 </div>

              <p class="mt-5 text-grey text-spacey"
                Think.<br>
                Capture.<br>
                Proceed.<br>
              </p>
            </div>
            <div class="col-xl-6">
              
            </div>
          </div>
          <div class="container py-5">
            <h1>Let the Hacking BEGIN</h1>
          </div>

          <div class="footer">
            <div class="row justify-content-center" style="text-align: center">
            </div>
            <div style="text-align: center">
              &copy; 2023 UIT.
            </div>
          </div>
      </div>
    </div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->

    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js" integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>

    <script src="assets/js/particles.js"></script>
    <script src="assets/js/app.js"></script>
  </body>
</html>
EOF;
  echo $html;
} else {
  $html = <<<EOF
<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>App - Home</title>

    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.6.3/css/all.css" integrity="sha384-UHRtZLI+pbxtHCWp1t77Bi1L4ZtiqrqD80Kn4Z8NTSRyMA2Fd33n5dQ8lWUE00s/" crossorigin="anonymous">
    
    <link rel="stylesheet" href="assets/css/bootstrap4-neon-glow.min.css">
    <link rel="stylesheet" href="assets/css/main.css">
    <link rel="stylesheet" href="assets/css/particles.css">
    
    <link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">
    <link rel='stylesheet' href='https://cdn.jsdelivr.net/font-hack/2.020/css/hack.min.css'>
    
  </head>
  <body>

  <div id="particles-js"></div>
    <div class="navbar-dark text-white">
      <div class="container">
        <nav class="navbar px-0 navbar-expand-lg navbar-dark">
          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
            <div class="navbar-nav">
              <a href="index.php" class="pl-md-0 p-3 text-light">Home</a>
              <a href="login.php" class="p-3 text-decoration-none text-light">Login</a>
              <a href="registration.php" class="p-3 text-decoration-none text-light active">Register</a>
            </div>
          </div>
        </nav>
  
      </div>
    </div>
    <div class="jumbotron bg-transparent mb-0 radius-0">
      <div class="container">
          <div class="row">
            <div class="col-xl-6">
              <h1 class="display-3">CAPTURE THE FLAG<span class="vim-caret">͏͏&nbsp;</span></h1>
              <div class="lead mb-3 text-mono text-success">Welcome hackers! Let me see if you can hack my supper secure app and steal some information from it.
              </div>
              <div class="text-mono">
                <a href="login.php"
                  title="Download Theme"
                  class="btn btn-success btn-shadow px-3 my-2 ml-0 text-left">
                  Login
                </a>
                <a href="registration.php"
                  class="btn btn-danger btn-shadow px-3 my-2 ml-0 ml-sm-1 text-left">
                  Register
                </a>
                
              </div>

              <div class="text-darkgrey text-mono my-2">We won't steal you passwords :)</div>

              <p class="mt-5 text-grey text-spacey">
                Think.<br>
                Capture.<br>
                Proceed.<br>
              </p>
            </div>
            <div class="col-xl-6">
              
            </div>
          </div>
          <div class="container py-5">
            <h1>Let the Hacking BEGIN</h1>
          </div>

          <div class="footer">
            <div style="text-align: center">
              &copy; 2023 UIT.
            </div>
          </div>
      </div>
    </div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->

    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js" integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>

    <script src="assets/js/particles.js"></script>
    <script src="assets/js/app.js"></script>
  </body>
</html>
EOF;
  echo $html;
}
