<?php
if(isset($_GET['source'])){
    highlight_file(__FILE__);
    die();
}

require('/var/www/vendor/smarty/smarty/libs/Smarty.class.php');
$smarty = new Smarty();
$smarty->setTemplateDir('/tmp/smarty/templates');
$smarty->setCompileDir('/tmp/smarty/templates_c');
$smarty->setCacheDir('/tmp/smarty/cache');
$smarty->setConfigDir('/tmp/smarty/configs');

$pattern = '/(\b)(on\S+)(\s*)=|javascript|<(|\/|[^\/>][^>]+|\/[^>][^>]+)>|({+.*}+)/';

if(!isset($_POST['data'])){
    $smarty->assign('pattern', $pattern);
    $smarty->display('index.tpl');
    exit();
}

// returns true if data is malicious
function check_data($data){
	global $pattern;
	return preg_match($pattern,$data);
}

if(check_data($_POST['data'])){
    $smarty->assign('pattern', $pattern);
    $smarty->assign('error', 'Malicious Inputs Detected');
    $smarty->display('index.tpl');
    exit();
}

$tmpfname = tempnam("/tmp/smarty/templates", "FOO");
$handle = fopen($tmpfname, "w");
fwrite($handle, $_POST['data']);
fclose($handle);
$just_file = end(explode('/',$tmpfname));
$smarty->display($just_file);
unlink($tmpfname);