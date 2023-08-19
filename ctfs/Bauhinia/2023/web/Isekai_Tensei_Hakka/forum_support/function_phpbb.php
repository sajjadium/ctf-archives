<?
//########## phpbb check begin ######### phpbb論壇專用

function phpbb_check($p_ip)
{
	global $db, $board_config;
	global $HTTP_COOKIE_VARS, $HTTP_GET_VARS, $SID,$root_path;
	$phpbb_root_path=$root_path;
	define('IN_PHPBB', true);
	include_once($root_path . 'extension.inc');
//	include_once($root_path . 'common.'.$phpEx);
	include_once($root_path . 'config.'.$phpEx);
	include_once($root_path . 'includes/constants.'.$phpEx);
	include_once($root_path . 'includes/sessions.'.$phpEx);
	include_once($root_path . 'includes/functions.'.$phpEx);
	include_once($root_path . 'includes/db.'.$phpEx);
	$board_config = array();
	$userdata = array();
	$user_ip = encode_ip($p_ip);
//	$user_ip = get_ip();
	$sql = "SELECT *
		FROM " . CONFIG_TABLE;
	if( !($result = $db->sql_query($sql)) )
	{
		message_die(CRITICAL_ERROR, "Could not query config information", "", __LINE__, __FILE__, $sql);
	}
	while ( $row = $db->sql_fetchrow($result) )
	{
		$board_config[$row['config_name']] = $row['config_value'];
	}
	if (file_exists('install') || file_exists('contrib'))
	{
		message_die(GENERAL_MESSAGE, 'Please ensure both the install/ and contrib/ directories are deleted');
	}
	$userdata = session_pagestart($user_ip, PAGE_WOG);
	$db->sql_close();
	return $userdata["user_id"];
}
?>