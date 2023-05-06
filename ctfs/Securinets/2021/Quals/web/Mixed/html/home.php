<?php session_start();include 'config.php';if(!isset($_SESSION['user'])){header('location:index.php');}?>
<html lang="en">
	<head>
		<meta charset="UTF-8" name="viewport" content="width=device-width, initial-scale=1"/>
		<link rel="stylesheet" type="text/css" href="css/bootstrap.css"/>
	</head>
<body>
	<nav class="navbar navbar-default">
		<div class="container-fluid">
			<a class="navbar-brand" href="home.php">Secret notes</a>
		</div>
	</nav>
	<div class="col-md-3"></div>
	<div class="col-md-6 well">
		<h3 class="text-primary">secret notes</h3>
		<hr style="border-top:1px dotted #ccc;"/>
		<a href="get.php">GET note</a>
		<h1>ADD note</h1>
		<form action='' method="POST" id="usrform">
			<input type="hidden" name="cook" value='<?php echo "cook=".my_encrypt($_SESSION['user'],$key);?>'>
			
			<input type="hidden" name="endpoint" value='add_note'>
			<input type="hidden" name="api" value="http://api.prodnotes.bb:5000/">
			<textarea rows="4" cols="50" name="comment" form="usrform">
Enter your secret note here...</textarea>
			<button class="btn btn-primary btn-block" name="submit"><span class="glyphicon glyphicon-save"></span> submit</button>
		</form>
		
	</div>
</body>
</html>
<?php
function my_encrypt($data, $passphrase) {
    $secret_key = hex2bin($passphrase);
    $iv = openssl_random_pseudo_bytes(openssl_cipher_iv_length('aes-256-cbc'));
    $encrypted_64 = openssl_encrypt($data, 'aes-256-cbc', $secret_key, 0, $iv);
    $iv_64 = base64_encode($iv);
    $json = new stdClass();
    $json->iv = $iv_64;
    $json->data = $encrypted_64;
    return base64_encode(json_encode($json));
} 

function check($url){
	$par=parse_url($url);
	if (((strpos($par['scheme'],'http')!==false)and($par['host']=='api.prodnotes.bb'))and($par['port']==5000)){
		return True;

	}
	else{
		return False;
	}

}
if (isset($_POST['submit'])){
	if ((isset($_POST['api']))and(isset($_POST['cook']))and(isset($_POST['endpoint']))and(isset($_POST['comment']))){
		$url=$_POST['api'].$_POST['endpoint'].'?comment='.urlencode($_POST['comment']).'&username='.$_SESSION['user'];
		if (check($url)){
			$opts = array(
  'http'=>array(
    'method'=>"GET",
    'follow_location'=>false,
    'header'=>"Accept-language: en\r\n" .
              "Cookie:".$_POST['cook']
  )
);
$context = stream_context_create($opts);
$file = file_get_contents($url, false, $context);
echo $file;

		}
	}
}
?>
