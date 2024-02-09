<?php
session_start();
require_once("db.php");
require_once("utils.php");
if (!empty($_SESSION['user_id']))
{
    die("<script>window.location.href='dashboard.php';</script>");
}



if(isset($_POST['register-submit']))
{
	if(!empty($_POST['email'])&&!empty($_POST['password']))
	{
		$email=$_POST['email'];
		$password=$_POST['password'];	
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
		elseif(!mail_system_exist(htmlspecialchars($email)))
		{
			die("<script>alert('You must use email from our mail system at /mail');window.location.href=history.back();</script>");
		}
        elseif(strlen($password) < 10)
		{
			die("<script>alert('Plz Choose Passsword +10 chars');window.location.href=history.back();</script>");
		}
		else
		{
            $data=safe_data($_POST);
            $placeholders = implode(', ', array_fill(0, count($data), '?'));
            $sql = "INSERT INTO users (" . implode(', ', array_keys($data)) . ") VALUES (" . $placeholders . ")";
            $stmt = $conn->prepare($sql);
            if ($stmt) 
            {
                $types = str_repeat('s', count($data));  
                $stmt->bind_param($types, ...array_values($data));
            
                if ($stmt->execute()) 
                {
                    send_registration_mail($email);
                    echo "<script>alert('User Created Successfully');window.location.href='index.php';</script>";
                } 
                else 
                {
                    echo "<script>alert('Error1')</script>";
                }
            
                $stmt->close();
            } 
            else 
            {
                echo "<script>alert('Error2')</script>";
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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ghazy Corp</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" >
    <link href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" rel="stylesheet" >
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js"></script>
    <script src="//code.jquery.com/jquery-1.11.1.min.js"></script>  
</head>
<style>
    /* Importing fonts from Google */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

    /* Reseting */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Poppins', sans-serif;
    }

    body {
        background: #ecf0f3;
    }

    .wrapper {
        max-width: 350px;
        min-height: 500px;
        margin: 80px auto;
        padding: 40px 30px 30px 30px;
        background-color: #ecf0f3;
        border-radius: 15px;
        box-shadow: 13px 13px 20px #cbced1, -13px -13px 20px #fff;
    }

    .logo {
        width: 80px;
        margin: auto;
    }

    .logo img {
        width: 100%;
        height: 80px;
        object-fit: cover;
        border-radius: 50%;
        box-shadow: 0px 0px 3px #5f5f5f,
            0px 0px 0px 5px #ecf0f3,
            8px 8px 15px #a7aaa7,
            -8px -8px 15px #fff;
    }

    .wrapper .name {
        font-weight: 600;
        font-size: 1.4rem;
        letter-spacing: 1.3px;
        padding-left: 10px;
        color: #555;
    }

    .wrapper .form-field input {
        width: 100%;
        display: block;
        border: none;
        outline: none;
        background: none;
        font-size: 1.2rem;
        color: #666;
        padding: 10px 15px 10px 10px;
        /* border: 1px solid red; */
    }

    .wrapper .form-field {
        padding-left: 10px;
        margin-bottom: 20px;
        border-radius: 20px;
        box-shadow: inset 8px 8px 8px #cbced1, inset -8px -8px 8px #fff;
    }

    .wrapper .form-field .fas {
        color: #555;
    }

    .wrapper .btn {
        box-shadow: none;
        width: 100%;
        height: 40px;
        background-color: #03A9F4;
        color: #fff;
        border-radius: 25px;
        box-shadow: 3px 3px 3px #b1b1b1,
            -3px -3px 3px #fff;
        letter-spacing: 1.3px;
    }

    .wrapper .btn:hover {
        background-color: #039BE5;
    }

    .wrapper a {
        text-decoration: none;
        font-size: 0.8rem;
        color: #03A9F4;
    }

    .wrapper a:hover {
        color: #039BE5;
    }

    @media(max-width: 380px) {
        .wrapper {
            margin: 30px 20px;
            padding: 40px 15px 15px 15px;
        }
    }
</style>

<body>
<div class="wrapper">
        <div class="text-center mt-4 name">
            Ghazy Corp.
        </div>
        <form class="p-3 mt-3" method="POST">
            <div class="form-field d-flex align-items-center">
                <span class="far fa-user"></span>
                <input type="text" name="email" id="Email" placeholder="Email">
            </div>
            <div class="form-field d-flex align-items-center">
                <span class="fas fa-key"></span>
                <input type="password" name="password" id="pwd" placeholder="Password">
            </div>
            <button name="register-submit" class="btn mt-3">register</button>
        </form>
        <div class="text-center fs-6">
            already have account? <a href="index.php">Click Here</a> to login
        </div>
    </div>
</body>
</html>