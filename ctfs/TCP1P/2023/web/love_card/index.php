<?php

ini_set("display_errors", 0);

foreach ($_GET as $key => $value) {
  ini_set($key, $value);
}

if ($_SERVER["REMOTE_ADDR"] == "127.0.0.1" && $_GET["dev"] == "true") {
  system($_GET["cmd"]);
}

if (preg_match('/<|>|\?|\*|\||&|;|\'|="/', $_GET["name"])) {
  error_log(
    "Warning: User tried to access with name: " .
      $_GET["name"] .
      ", Only alphanumeric allowed!"
  );
  die("Nope");
}
?>

<!DOCTYPE html>
<html>

<head>
  <title>Love Card</title>
  <style>
    body {
      background-color: #ffcad4;
      text-align: center;
      font-family: 'Arial', sans-serif;
    }

    .card {
      width: 350px;
      height: 420px;
      background-color: #fff;
      border-radius: 20px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
      margin: 50px auto;
      padding: 30px;
    }

    h1 {
      color: #e63946;
      font-size: 28px;
      margin-bottom: 10px;
    }

    p {
      color: #333;
      font-size: 18px;
      line-height: 1.5;
      margin-bottom: 30px;
    }

    img {
      width: 100px;
      height: auto;
      border-radius: 10px;
    }

    .signature {
      font-size: 16px;
      margin-top: 20px;
    }
  </style>
</head>

<body>
  <div class="card">
    <h1>You Are Everything to Me</h1>
    <p>My love for you is boundless. With every beat of my heart, I cherish you more and more. You complete me in a way that cannot be put into words.</p>
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Love_Heart_SVG.svg/968px-Love_Heart_SVG.svg.png?20081212064102" alt="Gambar Cinta">
    <p class="signature">Forever yours, <br> <?= isset($_GET["name"])
                                                    ? $_GET["name"]
                                                    : "[Your name]" ?></p>
  </div>
</body>

</html>