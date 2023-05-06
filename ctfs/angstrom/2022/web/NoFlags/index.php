<?php session_start(); ?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>No Flags?</title>
    <style>
        body {
            background-color: #f8bbd0;
        }

        h1, h2, li, input {
            color: #560027;
        }
        
        h1, h2 {
            font-family: sans-serif;
        }

        h1 {
            font-size: 36px;
        }

        h2 {
            font-size: 30px;
        }

        li, input {
            font-size: 24px;
            font-family: monospace;
        }

        input {
            background: none;
            border: 1px solid #880e4f;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>List of Fake Flags</h1>
    <ul>
    <?php
        if (!isset($_SESSION["DBNAME"])) {
            $dbname = hash("sha256", (string) rand());
            $_SESSION["DBNAME"] = $dbname;
            $init = true;
        } else {
            $dbname = $_SESSION["DBNAME"];
            $init = false;
        }
        $pdo = new PDO("sqlite:/tmp/$dbname.db");
        if ($init) {
            $pdo->exec("CREATE TABLE Flags (flag string); INSERT INTO Flags VALUES ('actf{not_the_flag}'), ('actf{maybe_the_flag}')");
        }
        if (isset($_POST["flag"])) {
            $flag = $_POST["flag"];
            $pdo->exec("INSERT INTO Flags VALUES ('$flag');");
        }
        foreach ($pdo->query("SELECT * FROM Flags") as $row) {
            echo "<li>" . htmlspecialchars($row["flag"]) . "</li>";
        }
    ?>
    </ul>
    <h2>Add a Fake Flag</h2>
    <form action="/" method="POST">
        <input type="text" name="flag" placeholder="flag...">
        <input type="submit" value="Add">
    </form>
</body>
</html>

