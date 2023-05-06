<?php
session_set_cookie_params(['samesite' => 'None','secure'=>'true']);
session_start();

function flash($severity, $content) {
	$_SESSION["flash"][] = array("severity" => $severity, "content" => $content);
}
