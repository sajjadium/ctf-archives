<?php ($_=$_SERVER['REQUEST_URI']) && (stripos($_,"zip") !== FALSE || stripos($_,"p:") || stripos($_,"s:")) && die("Bad hacker!");
($_=@$_GET['kaibro'].'.php') && @substr(file($_)[0],0,5) === '<?php' ? include($_) : highlight_file(__FILE__) && include('phpinfo.php');
