<?php

setcookie('AUTHKEY',"",time()-3600);

header("Location: http://".$_SERVER['HTTP_HOST']."/login.php");

?>

