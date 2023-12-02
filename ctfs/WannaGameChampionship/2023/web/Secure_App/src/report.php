<?php

session_start();
if (!@$_SESSION["isLoggedIn"]) {
    header("Location: /index.php");
    die();
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>App - CTF</title>

    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.6.3/css/all.css" integrity="sha384-UHRtZLI+pbxtHCWp1t77Bi1L4ZtiqrqD80Kn4Z8NTSRyMA2Fd33n5dQ8lWUE00s/" crossorigin="anonymous">

    <link rel="stylesheet" href="../assets/css/bootstrap4-neon-glow.min.css">
    <link rel="stylesheet" href="../assets/css/main.css">
    <link rel="stylesheet" href="../assets/css/particles.css">

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
                        <a href="/report.php" class="p-3 text-decoration-none text-light active">Report</a>
                    </div>
                </div>
            </nav>

        </div>
    </div>
    <div class="jumbotron bg-transparent mb-0 radius-0">
        <div class="container">
            <div class="row">


            </div>
            <div class="col-xl-6">

            </div>
        </div>
        <div class="container py-5 mb-5">

            <div class="row py-4">
                <div class="col-md-8 order-md-2">
                    <h4 class="mb-3">Report</h4>
                    <form method="POST">
                        <div class="mb-3">
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <span class="input-group-text">@</span>
                                </div>
                                <input type="password" class="form-control" id="url" name="url" placeholder="Your url goes here" required>
                            </div>
                        </div>
                        <hr class="mb-4">
                        <hr class="mb-4">
                        <button class="btn btn-outline-success btn-shadow btn-lg btn-block" type="submit"> Send </button>
                    </form>
                    <br>


                </div>
                <div class="col-md-2 order-md-1"></div>
                <div class="col-md-2 order-md-3"></div>
            </div>
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

</body>

</html>