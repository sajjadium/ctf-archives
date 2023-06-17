<?php 
    include("config.php");
    if(!is_login()) alert("login plz", "back");

    if(!isset($_SESSION["pow_prefix"])) {
        $prefix = shell_exec('python3 /tmp/gen_pow.py');
        $_SESSION["pow_prefix"] = trim($prefix);
    }

    if($_SERVER["REQUEST_METHOD"] == "POST") {
        if(isset($_SESSION["pow_prefix"]) && isset($_POST["url"]) && isset($_POST["pow"])) {
            if(verify_pow($_SESSION["pow_prefix"], $_POST["pow"])) {
                unset($_SESSION["pow_prefix"]);
                $address = gethostbyname("bot");
                $port = 5000;
                $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
        
                if ($socket === false) {
                    die("error! plz contact admin");
                }
                $result = socket_connect($socket, $address, $port);
        
                if ($result === false) {
                    die("error! plz contact admin");
                }
                socket_write($socket, $_POST["url"], strlen($_POST["url"]));
                socket_close($socket);
                die("<script> alert('Report Complete'); location.href='/'; </script>");
            } else {
                unset($_SESSION["pow_prefix"]);
                die("<script> alert('Invalid Pow'); location.href='/'; </script>");
            }
        } else {
            die("Invalid parameter");
        }
    }
?>
    sha256(<?=$prefix?> + ???) == 0000000000000000000000000000(28)...
    <br>
    <form action="/report.php" method="POST">
       url :  <input type="text" name="url" value="">
       pow : <input type="number" name="pow" value="">
       <input type="submit">
    </form>
