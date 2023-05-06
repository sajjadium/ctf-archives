<?php
ob_start();
error_reporting(0);
include ("config.php");
$file_name = $_GET['filename'];
$file_path = $_GET['filepath'];
$file_name=urldecode($file_name);
$file_path=urldecode($file_path);
$file = new File($file_name, $file_path);
$res = $file->view_detail();
$mine = $res['mine'];
$store_path = $res['store_path'];

echo <<<EOT
<div style="height: 30px; width: 1000px;">
<Ariel>mine: {$mine}</Ariel><br>
</div>
<div style="height: 30px; ">
<Ariel>file_path: {$store_path}</Ariel><br>
</div>
EOT;

ob_end_flush();
