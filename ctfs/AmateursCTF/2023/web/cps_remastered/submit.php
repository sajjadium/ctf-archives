<?php
if (isset($_POST["cps"]) && isset($_COOKIE["token"])) {
    $mysqli = new mysqli("p:db", "app", "ead549a4a7c448926bfe5d0488e1a736798a9a8ee150418d27414bd02d37b9e5", "cps");
    $stmt = $mysqli->prepare("SELECT best_cps FROM users WHERE username = (SELECT username FROM tokens WHERE token = ?)");
    $stmt->bind_param("s", $_COOKIE["token"]);
    $stmt->execute();
    $result = $stmt->get_result();
    $row = $result->fetch_assoc();
    if ($row["best_cps"] < $_POST["cps"] && (float) $_POST["cps"] < 1000) {
        $stmt = $mysqli->prepare("UPDATE users SET best_cps = ? WHERE username = (SELECT username FROM tokens WHERE token = ?)");
        $stmt->bind_param("ds", $_POST["cps"], $_COOKIE["token"]);
        $stmt->execute();
    }
    if ((float) $_POST["cps"] > 1000) {
        echo "CHEATER!!!";
    }
}
?>