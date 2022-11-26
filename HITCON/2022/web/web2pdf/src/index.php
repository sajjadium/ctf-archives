<?php
error_reporting(0);
require_once __DIR__ . '/../vendor/autoload.php';
require_once __DIR__ . '/hcaptcha.php';

if (isset($_GET['source']))
    die(preg_replace('#hitcon{\w+}#', 'h1tc0n{flag}', show_source(__FILE__, true)));


if (isset($_POST['url'])) {
    if (!verify_hcaptcha()) die("Captcha verification failed");
    $url = $_POST['url'];
    if (preg_match("#^https?://#", $url)) {
        $html = file_get_contents($url);
        $mpdf = new \Mpdf\Mpdf();
        $mpdf->WriteHTML($html);
        $mpdf->Output();
        exit;
    } else {
        die('Invalid URL');
    }
}

?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/awsm.css/dist/awsm.min.css">
    <title>web2pdf</title>
</head>

<body>
    <header>
        <h1>{web2pdf}</h1>
        <p>> Convert any web page to PDF online!</p>
        <nav>
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/?source">View Source Code</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <article>
            <section>
                <form method="POST" action="/">
                    <label for="url">URL</label>
                    <input id="url" name="url" type="text" placeholder="https://example.com/">
                    <input type="text" name="captcha" style="display: none">
                    <div class="h-captcha" data-sitekey="<?= $_ENV['HCAPTCHA_SITE_KEY'] ?>"></div>
                    <br>
                    <button>Submit</button>
                    <button type="reset">Reset</button>
                </form>
            </section>
        </article>
    </main>

    <script src="https://js.hcaptcha.com/1/api.js" async defer></script>
</body>

</html>

<?php  /* $FLAG = 'hitcon{redacted}' */ ?>