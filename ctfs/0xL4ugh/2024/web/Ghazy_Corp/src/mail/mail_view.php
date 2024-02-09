<?php
session_start();

require_once("../db.php");


if(!isset($_SESSION['mail_user_id']) || !isset($_GET['id']))
{
    die("<script>window.location.href='index.php';</script>");
}

$user_id=$_SESSION['mail_user_id'];
$stmt = $conn->prepare("select * from mails where id=?");
$stmt->bind_param("s", $_GET['id']);
$stmt->execute();
$res=$stmt->get_result();
if(!$res->num_rows > 0)
{
    die("Wrong Mail id");
}
$mail=$res->fetch_assoc();
$mail_owner=$mail['user_id'];

if($user_id !== $mail_owner)
{
    die("Unauthorized");
}

echo htmlspecialchars($mail['content'])."<br> <a href='mail.php'>Click Here to Back to mails list</a>";
?>