<?php

include 'class/User.php';

if (!empty($_POST))
{
	// serialise POST data for easy logging
	$loginAttempt = serialize((object)$_POST);

	// log access
	//Logger::log(Logger::SENSITIVE, 'Login attempt: ' . $loginAttempt);

	// Hand over to federation login
	// TODO currently just a mock up
	// TODO encrypt information to avoid loos of confidentiality
	header('Location: /?userdata=' . base64_encode($loginAttempt));
	die();
}

if (!empty($_GET) && isset($_GET['userdata']))
{
	// prepare notification data structure
	$notification = new stdClass();

	// check credentials & MFA
	try
	{
		$user = new User(base64_decode($_GET['userdata']));
		if ($user->verify())
		{
			$notification->type = 'success';
			$notification->text = 'Congratulations, your flag is: ' . file_get_contents('/flag.txt');
		}
		else
		{
			throw new InvalidArgumentException('Invalid credentials or MFA token value');
		}
	}
	catch (Exception $e)
	{
		$notification->type = 'danger';
		$notification->text = $e->getMessage();
	}
}

include 'template/home.html';
