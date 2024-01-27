<br><center>
<font size=5 color=red >STRESS RELEASE SERVICE</font>
<br><br><br>
To relieve all your stress from the old year, all you need is SHOUTTTTTT!!!!
<br><br><br>
<form action="/" method="GET">
	<input type="submit" value="shout"/><input type="text" name="shout" value="@!@!@!@!@!@!@!@!" />
</form>
</center>

<?php

function validateInput($input) {
    // To make your shout effective, it shouldn't contain alphabets or numbers.
    $pattern = '/[a-z0-9]/i';
    if (preg_match($pattern, $input)) {
        return false;
    } 

    // and only a few characters. Let's make your shout clean.
	$count = count(array_count_values(str_split($input)));
	if ($count > 7) {
		return false;
	}

	return true;
}

if (isset($_GET["shout"]) && !empty($_GET["shout"]) && is_string($_GET["shout"])) {
	$voice = $_GET["shout"];
	$res = "<center><br><br><img src=\"https://i.imgur.com/SvbbT0W.png\" width=5% /> WRONGGGGG WAYYYYYY TOOOO RELEASEEEEE STRESSSSSSSS!!!!!!</center>";
	if(validateInput($voice) === true) {
		eval("\$res='<center><br><br><img src=\"https://i.imgur.com/TL6siVW.png\" width=5% /> ".$voice.".</center>';");
	}

	if (strlen($res) < 300) {
		echo $res;
	} else {
		echo "<center>Too loud!!! Please respect your neighbor.</center>";
	}
} 

?>