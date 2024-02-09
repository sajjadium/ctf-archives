<?php
session_start();
require_once("../db.php");
require_once("../utils.php");
if (isset($_SESSION['mail_user_id']))
{
    die("<script>window.location.href='mail.php';</script>");
}



if(isset($_POST['login-submit']))
{
	if(!empty($_POST['email'])&&!empty($_POST['password']))
	{
		$email=$_POST['email'];
		$password=md5($_POST['password']);
		$stmt = $conn->prepare("select * from mail_users where email=? and password=?");
		$stmt->bind_param("ss", $email, $password);
		$stmt->execute();
		$res=$stmt->get_result();
		$user=$res->fetch_assoc();
		if($res->num_rows ===1)
		{
            $_SESSION["mail_user_id"]=$user['id'];
			$_SESSION["mail_mail"]=$user["email"];
			echo "<script>window.location.href='mail.php';</script>";
		}
		else
		{
			echo "<script>alert('Wrong Creds')</script>";
		}

	}
	else
	{
		echo "Please Fill All Fields";
	}
}
elseif(isset($_POST['register-submit']))
{
	if(!empty($_POST['email'])&&!empty($_POST['password'])&&!empty($_POST['confirm-password']))
	{
		$uuid=guidv4();
		$email=$_POST['email'];
		$password=$_POST['password'];
		$password2=$_POST['confirm-password'];		
		$stmt = $conn->prepare("select * from users where email=?");
		$stmt->bind_param("s", $email);
		$stmt->execute();
		$res=$stmt->get_result();
		if($res->num_rows ===1)
		{
			die("<script>alert('email taken');window.location.href=history.back();</script>");
		}
		elseif(!filter_var($email, FILTER_VALIDATE_EMAIL))
		{
			die("<script>alert('This is not valid email');window.location.href=history.back();</script>");
		}
		elseif($password!==$password2)
		{
			die("<script>alert('Passwords not equal');window.location.href=history.back();</script>");
		}
		elseif(strlen($password) < 10)
		{
			die("<script>alert('Plz Choose Passsword +10 chars');window.location.href=history.back();</script>");
		}
		else
		{
			$email=htmlspecialchars($email);
			$password=md5($password);
			$stmt = $conn->prepare("INSERT INTO  mail_users(id,email,password)values(?,?,?)");
			$stmt->bind_param("sss", $uuid,$email,$password);
			if($stmt->execute())
			{
                echo "<script>alert('User Created Successfully')</script>";
			}
			else
			{
				echo "<script>alert('Error')</script>";
			}
		}

		

	}
	else
	{
		echo "Please Fill All Fields";
	}
}





?>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mail System</title>
    <link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.0/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
    <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.0/js/bootstrap.min.js"></script>
    <script src="//code.jquery.com/jquery-1.11.1.min.js"></script>
</head>
<style>
	body {
    padding-top: 90px;
}
.panel-login {
	border-color: #ccc;
	-webkit-box-shadow: 0px 2px 3px 0px rgba(0,0,0,0.2);
	-moz-box-shadow: 0px 2px 3px 0px rgba(0,0,0,0.2);
	box-shadow: 0px 2px 3px 0px rgba(0,0,0,0.2);
}
.panel-login>.panel-heading {
	color: #00415d;
	background-color: #fff;
	border-color: #fff;
	text-align:center;
}
.panel-login>.panel-heading a{
	text-decoration: none;
	color: #666;
	font-weight: bold;
	font-size: 15px;
	-webkit-transition: all 0.1s linear;
	-moz-transition: all 0.1s linear;
	transition: all 0.1s linear;
}
.panel-login>.panel-heading a.active{
	color: #029f5b;
	font-size: 18px;
}
.panel-login>.panel-heading hr{
	margin-top: 10px;
	margin-bottom: 0px;
	clear: both;
	border: 0;
	height: 1px;
	background-image: -webkit-linear-gradient(left,rgba(0, 0, 0, 0),rgba(0, 0, 0, 0.15),rgba(0, 0, 0, 0));
	background-image: -moz-linear-gradient(left,rgba(0,0,0,0),rgba(0,0,0,0.15),rgba(0,0,0,0));
	background-image: -ms-linear-gradient(left,rgba(0,0,0,0),rgba(0,0,0,0.15),rgba(0,0,0,0));
	background-image: -o-linear-gradient(left,rgba(0,0,0,0),rgba(0,0,0,0.15),rgba(0,0,0,0));
}
.panel-login input[type="text"],.panel-login input[type="email"],.panel-login input[type="password"] {
	height: 45px;
	border: 1px solid #ddd;
	font-size: 16px;
	-webkit-transition: all 0.1s linear;
	-moz-transition: all 0.1s linear;
	transition: all 0.1s linear;
}
.panel-login input:hover,
.panel-login input:focus {
	outline:none;
	-webkit-box-shadow: none;
	-moz-box-shadow: none;
	box-shadow: none;
	border-color: #ccc;
}
.btn-login {
	background-color: #59B2E0;
	outline: none;
	color: #fff;
	font-size: 14px;
	height: auto;
	font-weight: normal;
	padding: 14px 0;
	text-transform: uppercase;
	border-color: #59B2E6;
}
.btn-login:hover,
.btn-login:focus {
	color: #fff;
	background-color: #53A3CD;
	border-color: #53A3CD;
}
.forgot-password {
	text-decoration: underline;
	color: #888;
}
.forgot-password:hover,
.forgot-password:focus {
	text-decoration: underline;
	color: #666;
}

.btn-register {
	background-color: #1CB94E;
	outline: none;
	color: #fff;
	font-size: 14px;
	height: auto;
	font-weight: normal;
	padding: 14px 0;
	text-transform: uppercase;
	border-color: #1CB94A;
}
.btn-register:hover,
.btn-register:focus {
	color: #fff;
	background-color: #1CA347;
	border-color: #1CA347;
}

</style>
<script>
$(function() {

	$('#login-form-link').click(function(e) {
		$("#login-form").delay(100).fadeIn(100);
		$("#register-form").fadeOut(100);
		$('#register-form-link').removeClass('active');
		$(this).addClass('active');
		e.preventDefault();
	});
	$('#register-form-link').click(function(e) {
		$("#register-form").delay(100).fadeIn(100);
		$("#login-form").fadeOut(100);
		$('#login-form-link').removeClass('active');
		$(this).addClass('active');
		e.preventDefault();
	});

});

</script>
<body>
<div class="container">
	<div class="row">
		<div class="col-md-6 col-md-offset-3">
			<div class="panel panel-login">
				<div class="panel-heading">
					<div class="row">
						<div class="col-xs-6">
							<a href="#" class="active" id="login-form-link">Login</a>
						</div>
						<div class="col-xs-6">
							<a href="#" id="register-form-link">Register</a>
						</div>
					</div>
					<hr>
				</div>
				<div class="panel-body">
					<div class="row">
						<div class="col-lg-12">
							<form id="login-form"  method="post" role="form" style="display: block;">
								<div class="form-group">
									<input type="text" name="email" id="username" tabindex="1" class="form-control" placeholder="Email" value="">
								</div>
								<div class="form-group">
									<input type="password" name="password" id="password" tabindex="2" class="form-control" placeholder="Password">
								</div>
								<div class="form-group">
									<div class="row">
										<div class="col-sm-6 col-sm-offset-3">
											<input type="submit" name="login-submit" id="login-submit" tabindex="4" class="form-control btn btn-login" value="Log In">
										</div>
									</div>
								</div>
							</form>
							<form id="register-form" enctype="multipart/form-data"  method="post" role="form" style="display: none;">
								<div class="form-group">
									<input type="email" name="email" id="email" tabindex="1" class="form-control" placeholder="Email Address" value="">
								</div>
								<div class="form-group">
									<input type="password" name="password" id="password" tabindex="2" class="form-control" placeholder="Password">
								</div>
								<div class="form-group">
									<input type="password" name="confirm-password" id="confirm-password" tabindex="2" class="form-control" placeholder="Confirm Password">
								</div>
								<div class="form-group">
									<div class="row">
										<div class="col-sm-6 col-sm-offset-3">
											<input type="submit" name="register-submit" id="register-submit" tabindex="4" class="form-control btn btn-register" value="Register Now">
										</div>
									</div>
								</div>
							</form>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>

    
</body>
</html>