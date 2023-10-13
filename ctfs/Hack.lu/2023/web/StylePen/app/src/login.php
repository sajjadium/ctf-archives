<?php
// my security guy told me to secure the staff pages 🤷
header("Content-Security-Policy: style-src 'self' 'unsafe-inline'; img-src *; script-src 'self' blob: 'wasm-unsafe-eval'; object-src 'none'; base-uri 'none';");

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    if (!is_string($_POST["username"]) || !is_string($_POST["password"])) {
        http_response_code(400);
        die("Invalid input");
    }
    include_once("include/DB.php");
    $username = login($_POST["username"], $_POST["password"]);
    if ($username) {
        $_SESSION["loggedin"] = true;
        $_SESSION["username"] = $username;
        $_SESSION["csrf"] = bin2hex(random_bytes(32));
        header("Location: /", true, 303);
        die();
    }
    $_SESSION["message"] = "Wrong username or password";
    $_SESSION["message_type"] = "error";
}
?>

<?php include_once("include/html_head.php") ?>
<main class="container">
    <h1>Staff login</h1>
    <form method="POST">
        <label for="username">Username</label>
        <input type="text" name="username" id="username" required>
        <label for="password">Password</label>
        <input type="password" name="password" id="password" required>
        <button type="submit" id="submit">Login</button>
    </form>
</main>