<?php

header("Creators: @CTFCreators");
session_start();
if( $_SESSION['loggedin'] != 1){
	header("Location: index.php");
}

include 'database.php';
$uname = $_SESSION['username'];

$isAdmin = 0;
if($uname == "admin"){
	$isAdmin = 1;
}

?>

<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" type="text/css" href="./css/CTFCreators.css">
	<title>Profile</title>
</head>
<body>
	<center>
		<h1 id=uname><?php echo "Welcome ".$uname; ?></h1>
		<h1 id=email></h1>

		<a id="logout" style="width:auto;" href="/logout.php">Logout</a>
		<?php if ($isAdmin ==1){?>
		
	</center>
	    <div class="container">
	      <label for="uname"><b>UUID</b></label>
	      <input type="text" id="uuid" placeholder="Enter UUID value" name="uuid" required>

	      <label for="psw"><b>Username</b></label>
	      <input type="text" placeholder="Username" name="username" id=user>
	        
	      <button type="submit" onclick="read()">Read</button>
	    </div>
	  <form class="modal-content animate"><input type="text" id="output" disabled></form>
	  <?php }?>
	<script type="text/javascript">
		xhr = new XMLHttpRequest()
		xhr.onreadystatechange = function(){
			document.getElementById("email").innerHTML = "E-Mail: "+this.responseText
		}
		xhr.open("get","data.php?u=<?php echo $uname;?>")
		xhr.send()

		function read(){
			var xml = '<\?xml version="1.0" encoding="UTF-8"?><user><username>'+document.getElementById("user").value+'</username></user>'

			var xhr = new XMLHttpRequest()
			xhr.onreadystatechange = function(){
				var out = document.getElementById("output")
				out.value = this.responseText
			}
			xhr.open("post","read.php")
			// 
			xhr.setRequestHeader("UUID", document.getElementById("uuid").value)
			xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded")
			xhr.send("data="+encodeURIComponent(xml))
		}
	</script>
</body>
</html>