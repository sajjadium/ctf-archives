<?
//########## vbb check begin ######### 2.X vbb論壇專用
function vbb_check()
{
	global $HTTP_COOKIE_VARS, $HTTP_GET_VARS,$root_path,$DB_site;
	// start server too busy
	$servertoobusy = 0;
	if ($loadlimit > 0)
	{
		$path = '/proc/loadavg';
		if(file_exists($path))
		{
			$filesize=filesize($path);
			$filenum=fopen($path,'r');
			$filestuff=@fread($filenum,6);
			fclose($filenum);
		} else {
			$filestuff = '';
		}
		$loadavg=explode(' ',$filestuff);
		if (trim($loadavg[0])>$loadlimit)
		{
			$servertoobusy=1;
		}
	}
	if (!$servertoobusy) {
		require($root_path.'/admin/functions.php');
		require($root_path.'/admin/sessions.php');
		
	} else {
		$session = array();
		$bbuserinfo = array();
	}
	return $bbuserinfo;
}
?>