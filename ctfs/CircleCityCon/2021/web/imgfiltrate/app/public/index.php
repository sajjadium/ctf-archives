<?php $nonce = "70861e83ad7f1863b3020799df93e450"; ?>
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width" />
        <title>imgfiltrate</title>
        <style>
body {
    font-family: -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif;
    padding: 2em;
}

h1 {
    margin-top: 2em;
    margin-bottom: 0;
}
</style>
        <meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self'; script-src 'nonce-<?php echo $nonce ?>';">
    </head>
    <body>
        <img id="flag" src="/flag.php">
        <p id="tag" hidden>Exfiltrate me</p>

        <script nonce=<?php echo $nonce ?>>
document.getElementById('flag').onmouseover = () => {
    document.getElementById('tag').hidden = false;
}

document.getElementById('flag').onmouseout = () => {
    document.getElementById('tag').hidden = true;
}
        </script>

        <h1>Hello <?php echo $_GET['name'] ?? 'bozo' ?></h1>
        <p>Unfortunately, only the admin can see the flag.</p>
    </body>
</html>
