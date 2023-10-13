<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <title>StylePen Spooktober Competition 2023</title>
    <link rel="icon" type="image/png" href="/static/ghost-favicon.png">
    <link rel="stylesheet" href="/static/pico.min.css">
    <link rel="stylesheet" href="/static/styles.css">
    <meta name="captcha-sitekey" content="<?= htmlentities(getenv('CAPTCHA_SITEKEY') ?: 'FCMV995O03V7RIMQ') ?>">
</head>

<body>
    <nav class="container-fluid">
        <ul>
            <li><a href="/">StylePen Spooktober Competition 2023</a></li>
        </ul>
        <ul>
            <?php if ($_SESSION['loggedin'] === true) : ?>
                <li>
                    Welcome back <?= htmlentities($_SESSION['username']) ?>!
                </li>
                <li>
                    <form class="inline-form" action="/logout.php" method='post'>
                        <input name="csrf" type="hidden" value="<?= htmlentities($_SESSION['csrf']) ?>">
                        <input role="button" type="submit" value="Logout">
                    </form>
                </li>
            <?php else : ?>
                <li><a href="/login.php">Staff Login</a></li>
            <?php endif ?>
        </ul>
        <div class="alert-container <?= htmlentities($_SESSION["message_type"]) ?: "hidden" ?>">
            <span class="alert-message"><?= htmlentities($_SESSION["message"]) ?></span>
            <span class="close-button">X</span>
        </div>
        <script src="/static/alert.js"></script>
        <?php unset($_SESSION["message"]); unset($_SESSION["message_type"]); ?>
    </nav>