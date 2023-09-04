<?php
    header("Content-Security-Policy: default-src 'none'; frame-ancestors 'none'; script-src 'unsafe-inline' 'unsafe-eval';");
    header("Cross-Origin-Opener-Policy: same-origin");

    $payload = "🚩🚩🚩";
    if (isset($_GET["xss"]) && is_string($_GET["xss"]) && strlen($_GET["xss"]) <= 30) {
        $payload = $_GET["xss"];
    }

    $flag = "SEKAI{test_flag}";
    if (isset($_COOKIE["flag"]) && is_string($_COOKIE["flag"])) {
        $flag = $_COOKIE["flag"];
    }
?>
<!DOCTYPE html>
<html>
    <body>
        <iframe
            sandbox="allow-scripts"
            srcdoc="<!-- <?php echo htmlspecialchars($flag) ?> --><div><?php echo htmlspecialchars($payload); ?></div>"
        ></iframe>
    </body>
</html>
