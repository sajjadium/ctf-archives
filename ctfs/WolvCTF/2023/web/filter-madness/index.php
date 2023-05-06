<?php
$result = 'no madness submitted yet';
$madness = isset($_GET['madness']) ? $_GET['madness'] : '';
if (strstr($madness, '/')) {
    die('Sorry, no slashes allowed');
}
$file = "php://filter/$madness/resource=/etc/passwd";
if (strlen($file) > 100) {
    die('Sorry, your madness is too long');
}
$result = file_get_contents($file);
if ($result === 'zombies for the flag') {
    $result = file_get_contents('/flag.txt');
}
?>
<div>Can you submit some madness that will return the flag?</div>
<br/>
<div>Your filter madness: <?php echo $file ?></div>
<div>Your filter madness length: <?php echo strlen($file) ?></div>
<div>Your filter madness results: <?php echo $result ?></div>
<br/>
<form method='GET'>
    <input name='madness'></input>
    <button>Submit</button>
</form>
<br/>
<div>Here's some <a href='/info.php'>info</a>.</div>