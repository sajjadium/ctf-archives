<?php

if($_SERVER['HTTP_X_SECURITY_DANGER']) {
?>
<!DOCTYPE html>

<head>
  <title>SECURITY ERROR</title>
  <link rel="stylesheet" href="app.css">
</head>

<body class="security">
  <p>🛑 SECURITY RISK DETECTED. ABORTING!! 🛑</p>
</body>

<?php
  exit;
}

if($_GET['file']) {
  $file = 'photos/' . $_GET['file'];
  if(file_exists($file)) {
    $fp = fopen($file, 'rb');

    header("Content-Type: image/jpeg");
    header("Content-Length: " . filesize($file));

    fpassthru($fp);

    exit;
  }
}
?>
<!DOCTYPE html>

<head>
  <title>My Photo Album 🐦</title>
  <link rel="stylesheet" href="app.css">
</head>

<body>
  <h1>🐦 My Pretty Bird Album 🐦</h1>

  <p class="small">Protected by UltraWAF™</p>

  <p>Click to see the full image!</p>

<?php
  $directory = array_diff(scandir('./photos/'), array('..', '.'));
  foreach($directory as $f) {
    print "<div class='cell'>";
    print "<a href='?file=$f'><img class='thumbnail' src='?file=$f' width=128 /></a>";
    print "</div>";
  }
?>
