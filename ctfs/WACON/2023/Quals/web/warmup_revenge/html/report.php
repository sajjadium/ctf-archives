<?php 
    include("config.php");
    if(!is_login()) die("login plz");

    if($_SERVER["REQUEST_METHOD"] == "GET") {
        if(isset($_GET["idx"]) && isset($_GET['path'])) {
            if(isset($_SESSION["report"]) && $_SESSION["report"] + 30 > time()) {
                die("Too fast");
            }

            if(!fetch_row('board', array('idx' => $_GET['idx'], 'username' => $_SESSION['username']), 'and'))  {
                die("Not found");
            }

            $address = gethostbyname("bot");
            $port = 5000;
            $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
    
            if($socket === false) {
                die("error! plz contact admin");
            }
            $result = socket_connect($socket, $address, $port);
    
            if($result === false) {
                die("error! plz contact admin");
            }
            $report_url = "http://webserver/".$_GET['path']."?p=read&idx=".$_GET['idx'];
            socket_write($socket, $report_url, strlen($report_url));
            socket_close($socket);
            $_SESSION["report"] = time();
            die("done");
        } else {
            die("Invalid parameter");
        }
    } else {
        die("nop");
    }
?>