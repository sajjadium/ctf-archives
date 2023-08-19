<?
//########## vbb check begin ######### 3.5.x vbb論壇專用
function vbb35_check()
{
	global $HTTP_COOKIE_VARS, $HTTP_GET_VARS,$root_path,$vbulletin;

define('VB_AREA', 'Forum');
define('THIS_SCRIPT', 'cron');
define('CWD',$root_path);

if (!defined('VB_AREA') AND !defined('THIS_SCRIPT'))
{
	echo 'VB_AREA or THIS_SCRIPT must be defined to continue';
	exit;
}

// start the page generation timer
$pagestarttime = microtime();
define('TIMESTART', microtime());

// set the current unix timestamp
define('TIMENOW', time());

// define current directory
if (!defined('CWD'))
{
	define('CWD', (($getcwd = getcwd()) ? $getcwd : '.'));
}

// #############################################################################
// fetch the core includes
require_once(CWD . '/includes/class_core.php');

// initialize the data registry
$vbulletin =& new vB_Registry();

// parse the configuration ini file
$vbulletin->fetch_config();

if (CWD == '.')
{
	// getcwd() failed and so we need to be told the full forum path in config.php
	if (!empty($vbulletin->config['Misc']['forumpath']))
	{
		define('DIR', $vbulletin->config['Misc']['forumpath']);
	}
	else
	{
		trigger_error('<strong>Configuration</strong>: You must insert a value for <strong>forumpath</strong> in config.php', E_USER_ERROR);
	}
}
else
{
	define('DIR', CWD);
}

if (!$vbulletin->debug)
{
	set_error_handler('vb_error_handler');
}

// #############################################################################
// load database class
switch (strtolower($vbulletin->config['Database']['dbtype']))
{
	// load standard MySQL class
	case 'mysql':
	case '':
	{
		if ($vbulletin->debug AND ($vbulletin->input->clean_gpc('r', 'explain', TYPE_UINT) OR (defined('POST_EXPLAIN') AND !empty($_POST))))
		{
			// load 'explain' database class
			require_once(DIR . '/includes/class_database_explain.php');
			$db =& new vB_Database_Explain($vbulletin);
		}
		else
		{
			$db =& new vB_Database($vbulletin);
		}
		break;
	}

	// load MySQLi class
	case 'mysqli':
	{
		if ($vbulletin->debug AND ($vbulletin->input->clean_gpc('r', 'explain', TYPE_UINT) OR (defined('POST_EXPLAIN') AND !empty($_POST))))
		{
			// load 'explain' database class
			require_once(DIR . '/includes/class_database_explain.php');
			$db =& new vB_Database_MySQLi_Explain($vbulletin);
		}
		else
		{
			$db =& new vB_Database_MySQLi($vbulletin);
		}
		break;
	}

	// load extended, non MySQL class
	default:
	{
	// this is not implemented fully yet
	//	$db = 'vB_Database_' . $vbulletin->config['Database']['dbtype'];
	//	$db =& new $db($vbulletin);
		die('Fatal error: Database class not found');
	}
}


// get core functions
if (!empty($db->explain))
{
	$db->timer_start('Including Functions.php');
	require_once(DIR . '/includes/functions.php');
	$db->timer_stop(false);
}
else
{
	require_once(DIR . '/includes/functions.php');
}

// make database connection
//echo $vbulletin->config['MasterServer']['username'];
$db->connect(
	$vbulletin->config['Database']['dbname'],
	$vbulletin->config['MasterServer']['servername'],
	$vbulletin->config['MasterServer']['port'],
	$vbulletin->config['MasterServer']['username'],
	$vbulletin->config['MasterServer']['password'],
	$vbulletin->config['MasterServer']['usepconnect'],
	$vbulletin->config['SlaveServer']['servername'],
	$vbulletin->config['SlaveServer']['port'],
	$vbulletin->config['SlaveServer']['username'],
	$vbulletin->config['SlaveServer']['password'],
	$vbulletin->config['SlaveServer']['usepconnect'],
	$vbulletin->config['Mysqli']['ini_file'],
	$vbulletin->config['Mysqli']['charset']
);

// make $db a member of $vbulletin
$vbulletin->db =& $db;

// vB 笢恅党蜊羲宎ㄩMySQL 4.1 眕奻唳掛觴鎢還奀賤樵源偶
if (empty($vbulletin->config['Mysqli']['ini_file']))
{
	$mysqlversion = $db->query_first("SELECT VERSION() AS version");

	define('MYSQL_VERSION', $mysqlversion['version']);

	if (MYSQL_VERSION >= '4.1')
	{
			$db->query("SET CHARACTER SET ".$vbulletin->config['Database']['charset']);
	}
}
// vB 笢恅党蜊賦旰


// #############################################################################
// fetch options and other data from the datastore
if (!empty($db->explain))
{
	$db->timer_start('Datastore Setup');
}

$datastore_class = (!empty($vbulletin->config['Datastore']['class'])) ? $vbulletin->config['Datastore']['class'] : 'vB_Datastore';

if ($datastore_class != 'vB_Datastore')
{
	require_once(DIR . '/includes/class_datastore.php');
}
$vbulletin->datastore =& new $datastore_class($vbulletin, $db);
$vbulletin->datastore->fetch($specialtemplates);

if ($vbulletin->bf_ugp === null)
{
// vB 笢恅党蜊羲宎: 楹祒
	echo '<div>vBulletin 杅擂遣湔渣昫ㄛ褫夔蚕ﾈ狟埻秪絳祡:
		<ol>
			' . (function_exists('mmcache_get') ? '<li>Turck MMCache 假蚾婓蠟腔督昢け笢ㄛ忑珂郭彸輦蚚 Turck MMCache 麼蔚〔杸遙峈 eAccelerator</li>' : '') . '
			<li>蠟褫夔奻換賸 vBulletin 3.5 腔恅璃ㄛ筍岆羶衄堍俴 vBulletin 3.5 汔撰最唗﹝ﾈ彆蠟羶衄堍俴汔撰最唗ㄛ饒繫ワ堍俴﹝</li>
			<li>Datastore 遣湔褫夔堤渣﹝ワ堍俴 <em>tools.php</em> 腔 <em>笭膘 Bitfields</em>﹝蠟褫眕婓 vBulletin ﾎ璃婦腔 <em>do_not_upload</em> 醴翹梑善涴跺恅璃﹝</li>
		</ol>
	</div>';

	trigger_error('vBulletin datastore 遣湔囮虴麼渣昫', E_USER_ERROR);
// vB 笢恅党蜊賦旰
}

if (!empty($db->explain))
{
	$db->timer_stop(false);
}

// #############################################################################
/**
* If shutdown functions are allowed, register exec_shut_down to be run on exit.
* Disable shutdown function for IIS CGI with Gzip enabled since it just doesn't work, sometimes, unless we kill the content-length header
*/
define('SAPI_NAME', php_sapi_name());
if (!defined('NOSHUTDOWNFUNC'))
{
	if ((SAPI_NAME == 'cgi' OR SAPI_NAME == 'cgi-fcgi') AND $vbulletin->options['gzipoutput'] AND strpos($_SERVER['SERVER_SOFTWARE'], 'Microsoft-IIS') !== false)
	{
		define('NOSHUTDOWNFUNC', true);
	}
	else
	{
		vB_Shutdown::add('exec_shut_down');
	}
}

// fetch url of referring page after we have access to vboptions['forumhome']
$vbulletin->url =& $vbulletin->input->fetch_url();
define('REFERRER_PASSTHRU', $vbulletin->url);

// #############################################################################
// referrer check for POSTs; this is simply designed to prevent self-submitting
// forms on foreign hosts from doing nasty things
if (strtoupper($_SERVER['REQUEST_METHOD']) == 'POST' AND !defined('SKIP_REFERRER_CHECK'))
{
	if ($_SERVER['HTTP_HOST'] OR $_ENV['HTTP_HOST'])
	{
		$http_host = ($_SERVER['HTTP_HOST'] ? $_SERVER['HTTP_HOST'] : $_ENV['HTTP_HOST']);
	}
	else if ($_SERVER['SERVER_NAME'] OR $_ENV['SERVER_NAME'])
	{
		$http_host = ($_SERVER['SERVER_NAME'] ? $_SERVER['SERVER_NAME'] : $_ENV['SERVER_NAME']);
	}

	if ($http_host AND $_SERVER['HTTP_REFERER'])
	{
		$referrer_parts = parse_url($_SERVER['HTTP_REFERER']);
		$ref_port = intval($referrer_parts['port']);
		$ref_host = $referrer_parts['host'] . (!empty($ref_port) ? ":$ref_port" : '');


		$allowed = preg_split('#\s+#', $vbulletin->options['allowedreferrers'], -1, PREG_SPLIT_NO_EMPTY);
		$allowed[] = preg_replace('#^www\.#i', '', $http_host);
		$allowed[] = '.paypal.com';

		$pass_ref_check = false;
		foreach ($allowed AS $host)
		{
			if (preg_match('#' . preg_quote($host, '#') . '$#siU', $ref_host))
			{
				$pass_ref_check = true;
				break;
			}
		}
		unset($allowed);

		if ($pass_ref_check == false)
		{
			die('In order to accept POST request originating from this domain, the admin must add this domain to the whitelist.');
		}
	}
}

// #############################################################################
// demo mode stuff
if (defined('DEMO_MODE') AND DEMO_MODE AND function_exists('vbulletin_demo_init'))
{
	vbulletin_demo_init();
}

// #############################################################################
// setup the hooks & plugins system
if ($vbulletin->options['enablehooks'] OR defined('FORCE_HOOKS'))
{
	require_once(DIR . '/includes/class_hook.php');
	$hookobj =& vBulletinHook::init();
	if ($vbulletin->options['enablehooks'] AND !defined('DISABLE_HOOKS'))
	{
		if (!empty($vbulletin->pluginlistadmin) AND is_array($vbulletin->pluginlistadmin))
		{
			$vbulletin->pluginlist = array_merge($vbulletin->pluginlist, $vbulletin->pluginlistadmin);
			unset($vbulletin->pluginlistadmin);
		}
		$hookobj->set_pluginlist($vbulletin->pluginlist);
	}
}
else
{
	// make a null class for optimization
	class vBulletinHook { function fetch_hook() { return false; } }
	$vbulletin->pluginlist = '';
}

($hook = vBulletinHook::fetch_hook('init_startup')) ? eval($hook) : false;

// #############################################################################
// do a callback to modify any variables that might need modifying based on HTTP input
// eg: doing a conditional redirect based on a $goto value or $vbulletin->noheader must be set
if (function_exists('exec_postvar_call_back'))
{
	exec_postvar_call_back();
}

// #############################################################################
// initialize $show variable - used for template conditionals
$show = array();

// #############################################################################
// Clean Cookie Vars
$vbulletin->input->clean_array_gpc('c', array(
	'vbulletin_collapse'            => TYPE_STR,
	COOKIE_PREFIX . 'referrerid' 	=> TYPE_UINT,
	COOKIE_PREFIX . 'userid' 		=> TYPE_UINT,
	COOKIE_PREFIX . 'password' 		=> TYPE_STR,
	COOKIE_PREFIX . 'lastvisit' 	=> TYPE_UINT,
	COOKIE_PREFIX . 'lastactivity' 	=> TYPE_UINT,
	COOKIE_PREFIX . 'threadedmode' 	=> TYPE_STR,
	COOKIE_PREFIX . 'sessionhash' 	=> TYPE_STR,
	COOKIE_PREFIX . 'styleid' 		=> TYPE_UINT,
	COOKIE_PREFIX . 'languageid'    => TYPE_UINT,
));

// #############################################################################
// Setup session
if (!empty($db->explain))
{
	$db->timer_start('Session Handling');
}

$vbulletin->input->clean_array_gpc('r', array(
	's'          => TYPE_STR,
	'styleid'    => TYPE_INT,
	'langid'     => TYPE_INT,
));

// conditional used in templates to hide things from search engines.
$show['search_engine'] = ($vbulletin->superglobal_size['_COOKIE'] == 0 AND preg_match("#(google|msnbot|yahoo! slurp)#si", $_SERVER['HTTP_USER_AGENT']));

// handle session input
$sessionhash = (!empty($vbulletin->GPC['s']) ? $vbulletin->GPC['s'] : $vbulletin->GPC[COOKIE_PREFIX . 'sessionhash']); // override cookie

// Set up user's chosen language
if ($vbulletin->GPC['langid'] AND !empty($vbulletin->languagecache["{$vbulletin->GPC['langid']}"]['userselect']))
{
	$languageid =& $vbulletin->GPC['langid'];
	vbsetcookie('languageid', $languageid);
}
else if ($vbulletin->GPC[COOKIE_PREFIX . 'languageid'] AND !empty($vbulletin->languagecache[$vbulletin->GPC[COOKIE_PREFIX . 'languageid']]['userselect']))
{
	$languageid = $vbulletin->GPC[COOKIE_PREFIX . 'languageid'];
}
else
{
	$languageid = 0;
}

// Set up user's chosen style
if ($vbulletin->GPC['styleid'])
{
	$styleid =& $vbulletin->GPC['styleid'];
	vbsetcookie('styleid', $styleid);
}
else if ($vbulletin->GPC[COOKIE_PREFIX . 'styleid'])
{
	$styleid = $vbulletin->GPC[COOKIE_PREFIX . 'styleid'];
}
else
{
	$styleid = 0;
}

// build the session and setup the environment
//echo $vbulletin;
$vbulletin->session =& new vB_Session($vbulletin, $sessionhash, $vbulletin->GPC[COOKIE_PREFIX . 'userid'], $vbulletin->GPC[COOKIE_PREFIX . 'password'], $styleid, $languageid);
// Google Web Accelerator can display sensitive data ignoring any headers regarding caching
// it's a good thing for guests but not for anyone else
if ($vbulletin->userinfo['userid'] > 0 AND strpos($_SERVER['HTTP_X_MOZ'], 'prefetch') !== false)
{
	if (SAPI_NAME == 'cgi' OR SAPI_NAME == 'cgi-fcgi')
	{
		header('Status: 403 Forbidden');
	}
	else
	{
		header('HTTP/1.1 403 Forbidden');
	}
	die('Prefetching is not allowed due to the various privacy issues that arise.');
}

// Hide sessionid in url if we are a search engine or if we have a cookie
$vbulletin->session->set_session_visibility($show['search_engine'] OR $vbulletin->superglobal_size['_COOKIE'] > 0);
$vbulletin->userinfo =& $vbulletin->session->fetch_userinfo();
$vbulletin->session->do_lastvisit_update($vbulletin->GPC[COOKIE_PREFIX . 'lastvisit'], $vbulletin->GPC[COOKIE_PREFIX . 'lastactivity']);
	return $vbulletin->userinfo['userid'];
}
?>