<?php
session_start();
function filter($url) {
	$black_lists = ['127.0.0.1', '0.0.0.0'];
	$url_parse = parse_url($url);
	$ip = gethostbyname($url_parse['host']);
    if (in_array($ip,$black_lists)) {
        return false;
    }
	return true;
}

if (isset($_SESSION['username'])) {
	if(isset($_POST['url'])) {
		$url = strtolower($_POST['url']);
		$check = filter($url);
		if (filter_var($url,FILTER_VALIDATE_URL,FILTER_FLAG_IPV4) && 
			preg_match('/(^https?:\/\/[^:\/]+)/',$url) && $check) {
            sleep(1);
			$ch = curl_init();
			curl_setopt($ch, CURLOPT_URL, $url);
			curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
            curl_setopt($ch, CURLOPT_FOLLOWLOCATION, false);
            curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 3);
            curl_setopt($ch, CURLOPT_TIMEOUT, 1);
			$output = curl_exec($ch);
			curl_close($ch);
		} else {
			die ("NO NO NO NO");
		}
	}
} else {
	header("Location: login.php");
    exit;
}
?>
<link href="//maxcdn.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
<script src="//maxcdn.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.min.js"></script>
<script src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<!------ Include the above in your HEAD tag ---------->

<!doctype html>
<html lang="en">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Fonts -->
    <link rel="dns-prefetch" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css?family=Raleway:300,400,600" rel="stylesheet" type="text/css">

    <link rel="stylesheet" href="css/style.css">

    <link rel="icon" href="Favicon.png">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css">

    <title>ISITDTU CTF</title>
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-light navbar-laravel">
    <div class="container">
        <a class="navbar-brand" href="/index.php">ISTDTU CTF</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>

    </div>
</nav>

<main class="login-form">
    <div class="cotainer">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">Capture</div>
                    <div class="card-body">
                        <form action="" method="POST">
                            <div class="form-group row">
                                <label for="email_address" class="col-md-4 col-form-label text-md-right">URL</label>
                                <div class="col-md-5">
                                    <input type="text" id="url" class="form-control" name="url" required autofocus>
                                </div>
                            </div>

                            <div class="col-md-4 offset-md-4">
                                <button type="submit" class="btn btn-primary" name="submit">
                                    Submit
                                </button>
                            </div>
                    </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
    </div>
    <h3><center><b>RESULT</b></center></h3>
    <?= $output; ?>
</main>
</body>
</html>
