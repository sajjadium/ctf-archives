
<?php

/*$date_logout = date('m'.'/'.'d'.'/'.'Y')." | ".date("h:i:sa");
$conn->query("update user set time_logout='$date_logout' where user_id='$session_id'");*/
 		
	 
	session_start();
	session_destroy();
    
 
	header('location:index.php');
    
?>