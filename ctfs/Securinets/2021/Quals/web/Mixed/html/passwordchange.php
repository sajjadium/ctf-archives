<?php
  session_start();
  if (!$_SESSION['user']) {
  session_destroy();
    header("Location: index.php");
    exit; 
  }
?>



<!DOCTYPE html>
<html>
<head>


  <meta http-equiv='content-type' content='text/html;charset=utf-8' />
  <title>change_password</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
<!--
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <link rel="stylesheet" href="styles.css" >
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script> 
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.0/jquery.min.js"></script>
-->
<link href="css/bootstrap.css" rel="stylesheet" />
<script src="jquery/jquery.min.js"></script>
<script src="js/bootstrap.min.js"></script>


<?php


$stusername=$_SESSION['user'];
echo "Username : ", $stusername;




?>


<script>

function updateValue(id, value)
{
    document.getElementById(id).value = value;
}

</script>

</head>



<body>

<?php
    $username = $_SESSION['user'];
?>

<fieldset>
<legend>Change My Password:</legend>


<form method="post">
<table align = center>
<tr>
<th>Field</th>
<th>Value</th>
</tr>

<tr>
<td>Username:</td>
<td><input type="text" name="username" value="<?php echo $username; ?>" size = 30 style="background-color:lightgrey" readonly ></td>
</tr>

<tr>
<td>Password:</td>
<td><input type="password" name="password" required style="background-color:yellow"></td>
</tr>

<tr><td><input type="submit" name="change" value="Change"></td></tr>
</table>
    </form>
</fieldset>

<?php
require_once 'conn.php';

if(isset($_POST['username']) and isset($_POST['password']))
{

    $query = "UPDATE member SET password=:password where username=:username";
    $stmt = $conn->prepare($query);
    $stmt->bindParam(':username', $username);
    $stmt->bindParam(':password', $_POST['password']);


        if($stmt->execute())
		{
			echo"Password Updated Successfully";
		}
		else
		{
			echo "Password Updation Failed";
		}


		
}


?>



</body>
</html>











