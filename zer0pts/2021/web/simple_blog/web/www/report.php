<?php
try {
  if (isset($_POST['param'])) {
    $redis = new Redis();
    $redis->connect("redis", 6379);
    $redis->rPush("query", $_POST['param']);
  }
} catch (Exception $e) {
  print($e);
  exit(0);
}
?>
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Report Vulnerability</title>
  </head>
  <body>
    <h1>Report Vulnerability</h1>
    <p>If you find a vulnerability in my blog platform, please report a Proof of Concept that exfiltrates <code>document.cookie</code> to me. I will check the URL with Mozilla Firefox later.</p>
    <p>I only accept reports under <code>/index.php</code>, so please submit only GET paremeters. For example, if the URL you want to submit is <code>http://example.com/index.php?theme=light</code>, please submit only <code>theme=light</code> part.</p>
    <form action="/report.php" method="post">
      <input type="text" name="param" placeholder="e.g. theme=light">
      <input type="submit" value="report">
    </form>
  </body>
</html>