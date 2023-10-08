<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Status Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        h1 {
            text-align: center;
        }
        .links {
            text-align: center;
            margin-top: 20px;
        }
        .link {
            text-decoration: none;
            margin-right: 20px;
            font-size: 18px;
        }
        hr {
            margin-top: 20px;
            border: 1px solid #ccc;
        }
        pre {
            background-color: #f5f5f5;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>System Status</h1>
    <div class="links">
        <a class="link" href="info.php?action=frontend">Frontend phpinfo</a>
        <a class="link" href="info.php?action=backend">Backend phpinfo</a>
        <a class="link" href="info.php?action=backend2">Backend system info</a>
    </div>
    <hr>
    <?php
    include("config.php");

    if(isset($_GET['action'])) {
        $action = $_GET['action'];
        if($action == "frontend") {
            die(phpinfo());
        } else if($action == "backend") {
            $backendInfo = file_get_contents("http://" . BACKEND_HOST . "/info.php");
            echo $backendInfo;
        } else if($action == "backend2") {
            $backendList = file_get_contents("http://" . BACKEND_HOST . "/list.php");
            echo "<pre>" . htmlspecialchars($backendList) . "</pre>";
        }
    }
    ?>
</body>
</html>