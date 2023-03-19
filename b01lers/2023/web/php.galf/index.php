<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>Welcome to the first ever Better PHP interpreter!!</h1>
    <h2>Note, this is still in development so there might be some weird output!</h2>
    <form action="/index.php" method="POST">
        <div class="">
            <label for="code" class="form-label">Code</label>
            <textarea class="form-control" id="code" name="code"></textarea>
        </div>
        <div class="">
            <label for="args" class="form-label">Args</label>
            <input type="text" class="form-control" id="args" name="args">
        </div>
        <div>
            <button type="submit" class="btn btn-primary">Run Code</button>
        </div>
    </form>
    <div>
        <p>Here is the output of your code:</p>
        <?php
            define('block', TRUE);
            require("parser/syntaxreader.php");
            include("flag.php");
            $code = NULL;
            $args = NULL;
            $result = NULL;
            if (isset($_POST['code']) && isset($_POST['args'])) {
                $code = $_POST['code'];
                $args = $_POST['args'];
                if (!isset($_COOKIE['DEBUG'])){
                    $result = new syntaxreader($code, $args);
                } 
                else if (strcmp($_COOKIE['DEBUG'], hash("md5", $flag)) == 0) {
                    echo "Warning: Adming debugging enabled!";
                    $result = new syntaxreader($code, $args, NULL);
                } else {
                    $debug = array("Debugging Enabled!", 69);
                    $result = new syntaxreader($code, $args, $debug);
                }
                $result->run();
            }
        ?>
    </div>
</body>
</html>