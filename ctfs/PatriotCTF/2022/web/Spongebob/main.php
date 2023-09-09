<?php
$text = $_POST['text'];
$command = "python3.9 memetext.py \"$text\"";
$out = shell_exec($command);
echo $out;
?>