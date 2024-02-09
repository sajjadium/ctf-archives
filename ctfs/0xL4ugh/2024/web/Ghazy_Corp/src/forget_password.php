<?php
session_start();

require_once('db.php');
require_once("utils.php");


if(isset($_POST['recover-submit']))
{
    if(!empty($_POST['email']))
    {
        $email=$_POST['email'];
        if(filter_var($email, FILTER_VALIDATE_EMAIL))
		{
            $stmt=$conn->prepare("select * from users where email=?");
            $stmt->bind_param("s", $email);
            $stmt->execute();
            $res=$stmt->get_result();
            if($res->num_rows > 0)
            {
                $target_user=$res->fetch_assoc();
                if($target_user['confirmed']===1)
                {
                    $level=(int)$target_user['level'];
                    generate_reset_tokens($email,$level);
                    send_forget_password_mail($email);
                    echo "<script>window.location.href='reset_password.php';</script>";
                }
                else
                {
                    die("<script>alert('Your Account is not confirmed');window.location.href='user_confirm.php';</script>");
                }
            }
            else
            {
                die("<script>alert('Your Email doesnt exist in our db');window.location.href=history.back();</script>");
            }
		}
        else
        {
            die("<script>alert('This is not valid email');window.location.href=history.back();</script>");
        }
    }
    else
    {
        die("<script>alert('Please Enter Your email');window.location.href=history.back();</script>");
    }
}



?>



<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css">
    <link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.0/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
    <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.0/js/bootstrap.min.js"></script>
    <script src="//code.jquery.com/jquery-1.11.1.min.js"></script>
    <title>Forget Password</title>
</head>
<style>
.form-gap {
padding-top: 70px;
}
</style>
<body>
    <div class="form-gap"></div>
    <div class="container">
    <div class="row">
        <div class="col-md-4 col-md-offset-4">
            <div class="panel panel-default">
                <div class="panel-body">
                <div class="text-center">
                    <h3><i class="fa fa-lock fa-4x"></i></h3>
                    <h2 class="text-center">Forgot Password?</h2>
                    <p>You can reset your password here.</p>
                    <div class="panel-body">

                    <form id="register-form" role="form" autocomplete="off" class="form" method="post">

                        <div class="form-group">
                        <div class="input-group">
                            <span class="input-group-addon"><i class="glyphicon glyphicon-envelope color-blue"></i></span>
                            <input id="email" name="email" placeholder="email address" class="form-control"  type="email">
                        </div>
                        </div>
                        <div class="form-group">
                        <input name="recover-submit" class="btn btn-lg btn-primary btn-block" value="Reset Password" type="submit">
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