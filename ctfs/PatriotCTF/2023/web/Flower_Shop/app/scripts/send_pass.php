<?php

$tmpPwd = $argv[1];
$wh = $argv[2];

$data = array('tmp_pass' => $tmpPwd);

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $wh);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);

$response = curl_exec($ch);

curl_close($ch);

?>