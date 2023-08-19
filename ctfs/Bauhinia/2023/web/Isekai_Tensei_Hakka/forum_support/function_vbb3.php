<?
//########## vbb check begin ######### 3.x vbb論壇專用
function vbb3_check()
{
	global $HTTP_COOKIE_VARS, $HTTP_GET_VARS,$root_path,$DB_site, $usercache, $vboptions, $vbphrase, $bbuserinfo, $permissions, $_USEROPTIONS, $phrasegroups, $usergroupcache;
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
		$_USEROPTIONS = array(
		'showsignatures'    => 1,
		'showavatars'       => 2,
		'showimages'        => 4,
		'coppauser'         => 8,
		'adminemail'        => 16,
		'showvcard'         => 32,
		'dstauto'           => 64,
		'dstonoff'          => 128,
		'showemail'         => 256,
		'invisible'         => 512,
		'showreputation'    => 1024,
		'receivepm'         => 2048,
		'emailonpm'         => 4096,
		'hasaccessmask'     => 8192,
		//'emailnotification' => 16384, // this value is now handled by the user.autosubscribe field
		'postorder'         => 32768,
	);
		require_once($root_path.'includes/config.php');
		define('TABLE_PREFIX', $tableprefix);
		define('COOKIE_PREFIX', (empty($cookieprefix)) ? 'bb' : $cookieprefix);
		define('DEBUG', !empty($debug));
//		require_once($root_path.'includes/init.php');

//--
	// load options, special templates and default language
	$optionsfound = false;
	if (defined('VB3UPGRADE'))
	{
		// ###################### Load vB2 Style Options #######################
		$DB_site->reporterror = 0;
		$optionstemp = $DB_site->query_first("SELECT template FROM template WHERE title = 'options'");
		$DB_site->reporterror = 1;
		if ($optionstemp)
		{
			eval($optionstemp['template']);
			$versionnumber = $templateversion;
			$optionsfound = true;
		}
		// work out the absolute path to vBulletin
		$_var = @strpos($bburl, '/', 8);
	}
	if (!defined('VB3INSTALL') AND $optionsfound === false)
	{
		// initialise
		$datastore = array();
		$vboptions = array();
		$forumcache = array();
		$usergroupcache = array();
		$stylechoosercache = array();

		if (!is_array($specialtemplates))
		{
			$specialtemplates = array();
		}

		// add default special templates
		if (!CACHE_DATASTORE_FILE OR !defined('CACHE_DATASTORE_FILE'))
		{
			$specialtemplates = array_merge(array(
				'options',
				'cron',
				'forumcache',
				'usergroupcache',
				'stylecache'
			), $specialtemplates);
		}
		else
		{
			require_once('./includes/datastore_cache.php');
			$optionsfound = !empty($vboptions);
			$specialtemplates = array_merge(array(
				'cron'
			), $specialtemplates);
		}

		if (!empty($specialtemplates))
		{
			$datastoretemp = $DB_site->query("
				SELECT title, data
				FROM " . TABLE_PREFIX . "datastore
				WHERE title IN ('" . implode("', '", array_map('addslashes', $specialtemplates)) . "')
			");
			unset($specials, $specialtemplates);

			while ($storeitem = $DB_site->fetch_array($datastoretemp))
			{
				switch($storeitem['title'])
				{
					// get $vboptions array
					case 'options':
					{
						$vboptions = unserialize($storeitem['data']);
						if (is_array($vboptions) AND isset($vboptions['languageid']))
						{
							$optionsfound = true;
						}
						if ($url == 'index.php')
						{
							$url = "$vboptions[forumhome].php";
						}
						$versionnumber = &$vboptions['templateversion'];
					}
					break;
					// get $forumcache array
					case 'forumcache':
					{
						$forumcache = unserialize($storeitem['data']);
					}
					break;

					// get $usergroupcache array
					case 'usergroupcache':
					{
						$usergroupcache = unserialize($storeitem['data']);
					}
					break;

					// Wol Spider information
					case 'wol_spiders':
					{
						$datastore['wol_spiders'] = unserialize($storeitem['data']);
					}
					break;

					// smiliecache information
					case 'smiliecache':
					{
						$smiliecache = unserialize($storeitem['data']);
					}
					break;

					case 'stylecache':
					{
						$stylechoosercache = unserialize($storeitem['data']);
					}
					break;

					// stuff the data into the $datastore array
					default:
					{
						$datastore["$storeitem[title]"] = $storeitem['data'];
					}
					break;
				}
			}
			// Fatal Error
			if (!$optionsfound)
			{
				require_once($root_path.'/includes/adminfunctions.php');
				require_once($root_path.'/includes/functions.php');
				$vboptions = build_options();
				if ($url == 'index.php')
				{
					$url = "$vboptions[forumhome].php";
				}
				$versionnumber = &$vboptions['templateversion'];
			}

			unset($storeitem);
			$DB_site->free_result($datastoretemp);
		}
	}
//---	
		require_once($root_path.'includes/functions.php');
		require_once($root_path.'includes/sessions.php');
	} else {
		$session = array();
		$bbuserinfo = array();
	}
	return $bbuserinfo;
}
?>