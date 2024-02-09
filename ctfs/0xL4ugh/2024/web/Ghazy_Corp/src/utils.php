<?php
error_reporting(0);
function generate_reset_tokens($email,$level)
{
    $_SESSION['reset_email']=$email;
    $_SESSION['reset_token1']=mt_rand();
    for($i=0;$i<$level;$i++)
    {
        mt_rand();
    }
    $_SESSION['reset_token2']=mt_rand();

    // Generating another values in case the user entered wrong token
    $_SESSION['reset_token3']=mt_rand();
    $_SESSION['reset_token4']=mt_rand();
}


function guidv4($data = null) {
    $data = $data ?? random_bytes(16);
    assert(strlen($data) == 16);
    $data[6] = chr(ord($data[6]) & 0x0f | 0x40);
    $data[8] = chr(ord($data[8]) & 0x3f | 0x80);
    return vsprintf('%s%s-%s-%s-%s-%s%s%s', str_split(bin2hex($data), 4));
}


function mail_system_exist($mail_system_email)
{
    global $conn;
    $mail_system_stmt=$conn->prepare("select * from mail_users where email=?");
    $mail_system_stmt->bind_param("s", $mail_system_email);
    $mail_system_stmt->execute();
    $mail_system_res=$mail_system_stmt->get_result();
    if ($mail_system_res->num_rows === 1)
    {
        return 1;
    }
    else
    {
        return 0;
    }


}

function send_registration_mail($email)
{
    global $conn;
    $email_id=guidv4();
    $email_content="Thank you for joining us, We Stopped account activation for a while due to an incedient. Please wait until we contact you again";
    $stmt=$conn->prepare("insert into mails(id,content,user_id) values(?,?,(select id from mail_users where email=?))");
    $stmt->bind_param("sss", $email_id,$email_content,$email);
    $stmt->execute();
}


function send_forget_password_mail($email)
{
    global $conn;
    $email_id=guidv4();
    $email_content="Here is your reset password tokens: ".$_SESSION['reset_token1'].", ".$_SESSION['reset_token2'];
    $stmt=$conn->prepare("insert into mails(id,content,user_id) values(?,?,(select id from mail_users where email=?))");
    $stmt->bind_param("sss", $email_id,$email_content,$email);
    $stmt->execute();
}


function safe_data($data)
{
    $keys=array_keys($data);
    $values=array_values($data);
    for($i=0;$i<count($data);$i++)
    {
        if ($keys[$i]==="register-submit")
        {
            continue;
        }
        $safe_key=preg_replace("/[^a-zA-Z0-9]/s","",$keys[$i]);
        $safe_value=preg_replace("/[^a-zA-Z0-9@\.]/s","",$values[$i]);
        if($safe_key==="password")
        {
            $safe_value=md5($safe_value);
        }
        
        $safe_array[$safe_key]=$safe_value;
    }
    
    return $safe_array;
}



?>


