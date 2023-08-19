<?
//########## DISCUZ check begin ######### DISCUZ論壇專用
function dz_check()
{
	global $HTTP_COOKIE_VARS, $HTTP_GET_VARS,$root_path,$DB_site;
	define('IN_DISCUZ', true);
	include_once($root_path.'./config.php');
	include_once($root_path.'./include/global.php');
	include_once($root_path.'./include/db_mysql.php');
	$db = new dbstuff;
	$db->connect($dbhost, $dbuser, $dbpw, $dbname, $pconnect);
	$db->select_db($dbname);
	unset($dbhost, $dbuser, $dbpw, $dbname, $pconnect);
	$table_sessions="cdb_sessions";
	$table_members="cdb_members";
	$sid = isset($_GET['sid']) ? $_GET['sid'] :(isset($_POST['sid']) ? $_POST['sid'] :$_COOKIE['sid']);

	$discuz_uid = $_COOKIE['_discuz_uid'];
	$discuz_pw = $_COOKIE['_discuz_pw'];
	$discuz_secques = $_COOKIE['_discuz_secques'];

	$userinfo="m.uid AS discuz_uid, m.username AS discuz_user, m.password AS discuz_pw,m.bank as userbank,m.money as usermoney, m.adminid, m.groupid, m.email, m.timeoffset,m.tpp, m.ppp, m.credit, m.timeformat, m.dateformat, m.signature, m.invisible, m.lastvisit, m.lastpost, m.newpm, m.accessmasks, m.regdate";

	if($sid) {
		if($discuz_uid) {
			$query = $db->query("SELECT s.sid, s.styleid, s.groupid='6' AS ipbanned, $userinfo FROM $table_sessions s, $table_members m WHERE m.uid=s.uid AND s.sid='$sid' AND CONCAT_WS('.',s.ip1,s.ip2,s.ip3,s.ip4)='$onlineip' AND m.uid='$discuz_uid' AND m.password='$discuz_pw' AND m.secques='$discuz_secques'");
		} else {
			$query = $db->query("SELECT sid, uid AS sessionuid, groupid, groupid='6' AS ipbanned, styleid FROM $table_sessions WHERE sid='$sid' AND CONCAT_WS('.',ip1,ip2,ip3,ip4)='$onlineip'");
		}
		if($_DSESSION = $db->fetch_array($query)) {
			$sessionexists = 1;
			if(!empty($_DSESSION['sessionuid'])) {
				$query = $db->query("SELECT $userinfo FROM $table_members m WHERE uid='$_DSESSION[sessionuid]'");
				$_DSESSION = array_merge($_DSESSION, $db->fetch_array($query));
			}
		} else {
			$query = $db->query("SELECT sid, groupid, groupid='6' AS ipbanned, styleid FROM $table_sessions WHERE sid='$sid' AND CONCAT_WS('.',ip1,ip2,ip3,ip4)='$onlineip'");
			if($_DSESSION = $db->fetch_array($query)) {
				clearcookies();
				$sessionexists = 1;
			}
		}
	}
	if(!$sessionexists) {
		if($discuz_uid) {
			$query = $db->query("SELECT $userinfo	FROM $table_members m WHERE uid='$discuz_uid' AND password='$discuz_pw' AND secques='$discuz_secques'");
			if(!($_DSESSION = $db->fetch_array($query))) {
				clearcookies();
			}
		}

		if(ipbanned($onlineip)) {
			$_DSESSION['ipbanned'] = 1;
		}

		$sid = random(6);
	}

	@extract($_DSESSION, EXTR_OVERWRITE);
	if(empty($discuz_uid) || empty($discuz_user)) {
		$discuz_user = '';
		$discuz_uid = $adminid = $credit =0;
		$groupid = $groupid != 6 ? 7 : 6;
	} else {
		$discuz_userss = $discuz_user;
		$discuz_user = addslashes($discuz_user);
		$credit = intval($credit);
	}
	$db->close();
	return $discuz_uid;
}
?>