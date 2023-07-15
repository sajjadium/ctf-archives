<!DOCTYPE html>
<html>

<head>
    <title>cps test</title>
</head>

<body>
    <h1>5 Second CPS test</h1>
    <?php
    $mysqli = new mysqli("p:db", "app", "ead549a4a7c448926bfe5d0488e1a736798a9a8ee150418d27414bd02d37b9e5", "cps");
    if (isset($_COOKIE["token"])) {
        $stmt = $mysqli->prepare("SELECT username FROM tokens WHERE token = ?");
        $stmt->bind_param("s", $_COOKIE["token"]);
        $stmt->execute();
        $result = $stmt->get_result();
        $row = $result->fetch_assoc();
        if ($row == null) {
            header("Location: /logout.php");
            die();
        }
        echo '<p>welcome, ' . substr($row["username"], 0, 5) . '. <a href="logout.php">log out</a></p>';
    } else {
        echo '<a href="register.php">register</a>
        <a href="login.php">login</a>';
    }

    echo '<h2>Leaderboard. {first 5 chars of username}:{first 5 chars of password}</h2>';
    echo '<ol>';
    $result = $mysqli->query("SELECT username, password, best_cps FROM users ORDER by best_cps DESC LIMIT 3");
    while ($row = $result->fetch_assoc()) {
        echo '<li>' . htmlspecialchars(substr($row["username"], 0, 5)) . ":" . htmlspecialchars(substr($row["password"], 0, 5)) . " with a cps of " . $row["best_cps"] . '</li>';
    }
    echo '</ol>';
    ?>
    <br />
    <button style="width: 600px; height:600px;" id="the">Click Here</button>
    <p>Current Cps: <span id="cps">0</span></p>
    <script>
        let button = document.getElementById("the");
        let running = 0;
        let clicks = 0;
        button.onclick = () => {
            if (running) {
                clicks++;
            } else {
                running = performance.now();
                requestAnimationFrame(loop);
            }
        }

        function loop(t) {
            const timeElapsed = t - running;
            document.getElementById("cps").innerHTML = (clicks / (timeElapsed / 1000)).toFixed(2);
            if (timeElapsed > 5000) {
                <?php
                if ($_COOKIE["token"]) {
                    ?>
                    let data = new FormData();
                    data.append("cps", (clicks / (timeElapsed / 1000)));
                    fetch("submit.php", { method: "POST", body: data })
            <?php
                }
                ?>
                running = 0;
                clicks = 0;
                button.disabled = true;
                setTimeout(() => button.disabled = false, 2000);
            } else {
                requestAnimationFrame(loop);
            }
        }
    </script>
</body>

</html>