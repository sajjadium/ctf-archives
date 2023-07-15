<?php
define('ENABLE_RECAPTCHA', getenv('ENABLE_RECAPTCHA') === 'yes');
define('RECAPTCHA_SITE_KEY', getenv('RECAPTCHA_SITE_KEY'));
define('RECAPTCHA_SECRET_KEY', getenv('RECAPTCHA_SECRET_KEY'));

try {
    if (isset($_POST['id'])) {
        if (ENABLE_RECAPTCHA) {
            if (!isset($_POST['token'])) {
                die('reCAPTCHA failed');
            }

            $data = 'secret=' . RECAPTCHA_SECRET_KEY . '&response=' . urlencode($_POST['token']);
            $headers = [
                'Content-Type: application/x-www-form-urlencoded',
                'Content-Length: ' . strlen($data)
            ];
            $resp = file_get_contents('https://www.google.com/recaptcha/api/siteverify', false, stream_context_create([
                'http' => [
                    'method' => 'POST',
                    'header' => implode("\r\n", $headers),
                    'content' => $data
                ]
            ]));
    
            $resp = json_decode($resp, true);
            if (!$resp['success']) {
                die('reCAPTCHA failed');
            }
        }

        $id = $_POST['id'];
        if (strlen($id) > 1000) {
            die('id too long');
        }

        $redis = new Redis();
        $redis->connect("redis", 6379);
        $redis->rPush("report", $id);
        die('Successfully reported');
    }
} catch (Exception $e) {
    print($e);
    exit(0);
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Appeal to admin to add 1,000 likes</title>
    <link href="/style.css" rel="stylesheet">
</head>
<body>
    <h1>Plain Blog - Frontend Example</h1>
    <h2>Appeal to admin to add 1,000 likes</h2>
    <p>Submit your post ID here. Admin will check it and give likes to it later.</p>
    <div>
        <label>ID: <input type="text" name="id" id="id" placeholder="00000000-0000-0000-0000-000000000000" size="40"></label><br>
        <?php if (ENABLE_RECAPTCHA) { ?>
        <button class="g-recaptcha" 
            data-sitekey="<?= RECAPTCHA_SITE_KEY ?>" 
            data-callback='onSubmit' 
            data-action='submit'>Submit</button>
        <?php } else { ?>
        <button onclick="onSubmit();">Submit</button>
        <?php } ?>
    </div>
    <output id="output"></output>
    <?php if (ENABLE_RECAPTCHA) { ?>
    <script src="https://www.google.com/recaptcha/api.js"></script>
    <?php } ?>
    <script>
    async function onSubmit(token) {
        const output = document.getElementById('output');

        const id = document.getElementById('id').value;
        let formData = new FormData();
        formData.append('id', id);
        formData.append('token', token);

        const res = await (await fetch('/report.php', {
            method: 'POST',
            body: formData
        })).text();
        
        output.textContent = res;
        return false;
    }
    </script>
</body>
</html>