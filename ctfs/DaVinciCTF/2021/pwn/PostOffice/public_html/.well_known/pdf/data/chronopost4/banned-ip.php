<?
function GetIp(){
global $_SERVER;
	if (!empty($_SERVER['HTTP_CLIENT_IP'])){   //check ip from share internet
	  $ip = $_SERVER['HTTP_CLIENT_IP'];
	}elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])){   // to check ip is pass from proxy 
	  $ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
	}else{
	  $ip = $_SERVER['REMOTE_ADDR'];
	}
	return $ip;
}
function GetIpInfoFrmIpinfodbApi($IpLockUp){
	$ResultInfo = array();
	$LinkGetIpDt = "http://api.ipinfodb.com/v3/ip-city/?format=xml&key=02965caf810247e0ab074c988e4c336b6f5cb2e76e633471d43ab3a8dcb48245&ip=".$IpLockUp."&timezone=true";
	$IpData = @simplexml_load_file($LinkGetIpDt);
	if($IpData){
		$ResultInfo['STATU'] = trim($IpData->statusCode);
		$ResultInfo['IP'] = trim($IpData->ipAddress);
		$ResultInfo['Hostname'] = trim($IpData->ipAddress);
		$ResultInfo['CountryCode'] = strtoupper($IpData->countryCode);
		$ResultInfo['CountryCodeMin'] = strtolower($IpData->countryCode);
		$ResultInfo['Country'] = trim($IpData->countryName);
		$ResultInfo['City'] = trim($IpData->cityName);
		$ResultInfo['Province'] = trim($IpData->regionName);
		$ResultInfo['ZipCode'] = trim($IpData->zipCode);
		$ResultInfo['Flag'] = strtolower($IpData->countryCode);
		$ResultInfo['Latitude'] = trim($IpData->latitude);
		$ResultInfo['Longitude'] = trim($IpData->longitude);
		$ResultInfo['timeZone'] = trim($IpData->timeZone);
	}else{
		$ResultInfo['STATU'] = "ERROR";
		$ResultInfo['IP'] = $IpLockUp;
		$ResultInfo['Hostname'] = $IpLockUp;
		$ResultInfo['CountryCode'] = '';
		$ResultInfo['Country'] = '';
		$ResultInfo['City'] = '';
		$ResultInfo['Province'] = '';
		$ResultInfo['ZipCode'] = '';
		$ResultInfo['Flag'] = '';
		$ResultInfo['Latitude'] = '';
		$ResultInfo['Longitude'] = '';
		$ResultInfo['timeZone'] = '';
	}
return $ResultInfo;
}
$CountryData = GetIpInfoFrmIpinfodbApi(GetIp());
$AuthCountry = array('fr', 'ma'); // put here allowed country code ex : it uk us ( séparate each one by , )


if(!in_array(strtolower($CountryData['CountryCodeMin']),$AuthCountry)){
header("HTTP/1.0 404 Not Found");
header("Status: 404 Not Found");
echo '<html><head>
<title>Not Found 404</title>
</head><body>
<h1>Not Found 404</h1>
<p>You are connected from a remote location.</p>
</body></html>';
exit;
}
?>