<?
//########## DISCUZ check begin ######### DISCUZ論壇專用
function dz_check()
{
	global $HTTP_COOKIE_VARS, $HTTP_GET_VARS,$root_path,$DB_site;
	define('IN_DISCUZ', true);
	require_once $root_path.'./include/global.func.php';

	$magic_quotes_gpc = get_magic_quotes_gpc();
	$register_globals = @ini_get('register_globals');

	if(!$register_globals || !$magic_quotes_gpc) {
		@extract(daddslashes($_POST));
		@extract(daddslashes($_GET));
		if(!$magic_quotes_gpc) {
			$_FILES = daddslashes($_FILES);
		}
	}

	$charset = $dbcharset = '';
	$plugins = $hooks = array();

	require_once $root_path.'./config.inc.php';
	require_once $root_path.'./include/db_mysql.class.php';

	if($attackevasive) {
		require_once $root_path.'./include/security.inc.php';
	}

	$timestamp = time();
	$PHP_SELF = $_SERVER['PHP_SELF'] ? $_SERVER['PHP_SELF'] : $_SERVER['SCRIPT_NAME'];
	$SCRIPT_FILENAME = str_replace('\\\\', '/', ($_SERVER['PATH_TRANSLATED'] ? $_SERVER['PATH_TRANSLATED'] : $_SERVER['SCRIPT_FILENAME']));
	$boardurl = 'http://'.$_SERVER['HTTP_HOST'].preg_replace("/\/+(api|archiver|wap)?\/*$/i", '', substr($PHP_SELF, 0, strrpos($PHP_SELF, '/'))).'/';

//$adminemail = emailconv($adminemail, 0);

	$extrahead = '';
	$_DCOOKIE = $_DSESSION = $_DCACHE = $_DPLUGIN = array();

	$prelength = strlen($tablepre);
	foreach($_COOKIE as $key => $val) {
		if(substr($key, 0, $prelength) == $tablepre) {
			$_DCOOKIE[(substr($key, $prelength))] = daddslashes($val);
		}
	}
	unset($prelength);

	if(getenv('HTTP_CLIENT_IP') && strcasecmp(getenv('HTTP_CLIENT_IP'), 'unknown')) {
		$onlineip = getenv('HTTP_CLIENT_IP');
	} elseif(getenv('HTTP_X_FORWARDED_FOR') && strcasecmp(getenv('HTTP_X_FORWARDED_FOR'), 'unknown')) {
		$onlineip = getenv('HTTP_X_FORWARDED_FOR');
	} elseif(getenv('REMOTE_ADDR') && strcasecmp(getenv('REMOTE_ADDR'), 'unknown')) {
		$onlineip = getenv('REMOTE_ADDR');
	} elseif(isset($_SERVER['REMOTE_ADDR']) && $_SERVER['REMOTE_ADDR'] && strcasecmp($_SERVER['REMOTE_ADDR'], 'unknown')) {
		$onlineip = $_SERVER['REMOTE_ADDR'];
	}
	$onlineip = preg_replace("/^([\d\.]+).*/", "\\1", $onlineip);

	$cachelost = (@include $root_path.'./forumdata/cache/cache_settings.php') ? '' : 'settings';
	@extract($_DCACHE['settings']);

	$db = new dbstuff;
	$db->connect($dbhost, $dbuser, $dbpw, $dbname, $pconnect);
	unset($dbhost, $dbuser, $dbpw, $dbname, $pconnect);

	$sid = daddslashes(($transsidstatus || (defined('CURSCRIPT') && CURSCRIPT == 'wap'))&& (isset($_GET['sid']) || isset($_POST['sid'])) ?
		(isset($_GET['sid']) ? $_GET['sid'] : $_POST['sid']) :
		(isset($_DCOOKIE['sid']) ? $_DCOOKIE['sid'] : ''));

	$discuz_auth_key = md5($_DCACHE['settings']['authkey'].$_SERVER['HTTP_USER_AGENT']);
	list($discuz_pw, $discuz_secques, $discuz_uid) = isset($_DCOOKIE['auth']) ? explode("\t", authcode($_DCOOKIE['auth'], 'DECODE','$discuz_auth_key')) : array('', '', 0);

	if(isset($_DCOOKIE['auth']) && !$discuz_uid) {
		clearcookies();
	}

	$newpm = $newpmexists = $sessionexists = $seccode = $bloguid = 0;
	if($sid) {
		if($discuz_uid) {
			$query = $db->query("SELECT s.sid, s.styleid, s.groupid='6' AS ipbanned, s.pageviews AS spageviews, s.lastolupdate, s.seccode, m.uid AS discuz_uid,
				m.username AS discuz_user, m.password AS discuz_pw, m.secques AS discuz_secques, m.adminid, m.groupid, m.groupexpiry,
				m.extgroupids, m.email, m.timeoffset, m.tpp, m.ppp, m.posts, m.digestposts, m.oltime, m.pageviews, m.credits, m.extcredits1, m.extcredits2, m.extcredits3,
				m.extcredits4, m.extcredits5, m.extcredits6, m.extcredits7, m.extcredits8, m.timeformat, m.dateformat, m.pmsound,
				m.sigstatus, m.invisible, m.lastvisit, m.lastactivity, m.lastpost, m.newpm, m.accessmasks
				FROM {$tablepre}sessions s, {$tablepre}members m
				WHERE m.uid=s.uid AND s.sid='$sid' AND CONCAT_WS('.',s.ip1,s.ip2,s.ip3,s.ip4)='$onlineip' AND m.uid='$discuz_uid'
				AND m.password='$discuz_pw' AND m.secques='$discuz_secques'");
		} else {
			$query = $db->query("SELECT sid, uid AS sessionuid, groupid, groupid='6' AS ipbanned, pageviews AS spageviews, styleid, lastolupdate, seccode
				FROM {$tablepre}sessions WHERE sid='$sid' AND CONCAT_WS('.',ip1,ip2,ip3,ip4)='$onlineip'");
		}
			if($_DSESSION = $db->fetch_array($query)) {
			$sessionexists = 1;
			if(!empty($_DSESSION['sessionuid'])) {
				$query = $db->query("SELECT m.uid AS discuz_uid, m.username AS discuz_user, m.password AS discuz_pw,
					m.secques AS discuz_secques, m.adminid, m.groupid, m.groupexpiry, m.extgroupids, m.email, m.timeoffset,
					m.tpp, m.ppp, m.posts, m.digestposts, m.oltime, m.pageviews, m.credits, m.extcredits1, m.extcredits2, m.extcredits3, m.extcredits4, m.extcredits5,
					m.extcredits6, m.extcredits7, m.extcredits8, m.timeformat, m.dateformat, m.pmsound, m.sigstatus, m.invisible,
					m.lastvisit, m.lastactivity, m.lastpost, m.newpm, m.accessmasks
					FROM {$tablepre}members m WHERE uid='$_DSESSION[sessionuid]'");
				$_DSESSION = array_merge($_DSESSION, $db->fetch_array($query));
			}
		} else {
			$query = $db->query("SELECT sid, groupid, groupid='6' AS ipbanned, pageviews AS spageviews, styleid, lastolupdate, seccode
				FROM {$tablepre}sessions WHERE sid='$sid' AND CONCAT_WS('.',ip1,ip2,ip3,ip4)='$onlineip'");
			if($_DSESSION = $db->fetch_array($query)) {
				clearcookies();
				$sessionexists = 1;
			}
		}
	}

	if(!$sessionexists) {
		if($discuz_uid) {
			$query = $db->query("SELECT uid AS discuz_uid, username AS discuz_user, password AS discuz_pw, secques AS discuz_secques,
				adminid, groupid, groupexpiry, extgroupids, email, timeoffset, styleid, tpp, ppp, posts, digestposts, oltime, pageviews, credits,
				extcredits1, extcredits2, extcredits3, extcredits4, extcredits5, extcredits6, extcredits7, extcredits8, timeformat,
				dateformat, pmsound, sigstatus, invisible, lastvisit, lastactivity, lastpost, newpm, accessmasks
				FROM {$tablepre}members WHERE uid='$discuz_uid' AND password='$discuz_pw' AND secques='$discuz_secques'");
			if(!($_DSESSION = $db->fetch_array($query))) {
				clearcookies();
			}
		}

		if(ipbanned($onlineip)) {
			$_DSESSION['ipbanned'] = 1;
		}

		$_DSESSION['sid'] = random(6);
		$_DSESSION['seccode'] = random(4, 1);
	}

	$_DSESSION['dateformat'] = empty($_DSESSION['dateformat']) ? $_DCACHE['settings']['dateformat'] : $_DSESSION['dateformat'];
	$_DSESSION['timeformat'] = empty($_DSESSION['timeformat']) ? $_DCACHE['settings']['timeformat'] : ($_DSESSION['timeformat'] == 1 ? 'h:i A' : 'H:i');
	$_DSESSION['timeoffset'] = isset($_DSESSION['timeoffset']) && $_DSESSION['timeoffset'] != 9999 ? $_DSESSION['timeoffset'] : $_DCACHE['settings']['timeoffset'];

	@extract($_DSESSION);

	$lastvisit = empty($lastvisit) ? $timestamp - 86400 : $lastvisit;
	$timenow = array('time' => gmdate("$dateformat $timeformat", $timestamp + 3600 * $timeoffset),
		'offset' => ($timeoffset >= 0 ? ($timeoffset == 0 ? '' : '+'.$timeoffset) : $timeoffset));

	if(empty($discuz_uid) || empty($discuz_user)) {
		$discuz_user = $extgroupids = '';
		$discuz_uid = $adminid = $posts = $digestposts = $pageviews = $oltime = $invisible
			= $credits = $extcredits1 = $extcredits2 = $extcredits3 = $extcredits4
			= $extcredits5 = $extcredits6 = $extcredits7 = $extcredits8 = 0;
		$groupid = empty($groupid) || $groupid != 6 ? 7 : 6;
		$avatarshowid = 0;
	} else {
		$discuz_userss = $discuz_user;
		$discuz_user = addslashes($discuz_user);
	}

	$db->close();
	return $discuz_uid;
}
?>