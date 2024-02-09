<?php
session_start();
require_once("../db.php");
if(!isset($_SESSION['mail_user_id']))
{
    die("<script>window.location.href='index.php';</script>");
}
$user_id=$_SESSION['mail_user_id'];
$stmt = $conn->prepare("select * from mails where user_id=?");
$stmt->bind_param("s", $user_id);
$stmt->execute();
$res=$stmt->get_result();




?>

<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mail System</title>
    <link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
    <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js"></script>
    <script src="//code.jquery.com/jquery-1.11.1.min.js"></script>
</head>
<style>
    /* CSS used here will be applied after bootstrap.css */

    body{ margin-top:50px;}
    .nav-tabs .glyphicon:not(.no-margin) { margin-right:10px; }
    .tab-pane .list-group-item:first-child {border-top-right-radius: 0px;border-top-left-radius: 0px;}
    .tab-pane .list-group-item:last-child {border-bottom-right-radius: 0px;border-bottom-left-radius: 0px;}
    .tab-pane .list-group .checkbox { display: inline-block;margin: 0px; }
    .tab-pane .list-group input[type="checkbox"]{ margin-top: 2px; }
    .tab-pane .list-group .glyphicon { margin-right:5px; }
    .tab-pane .list-group .glyphicon:hover { color:#FFBC00; }
    a.list-group-item.read { color: #222;background-color: #F3F3F3; }
    hr { margin-top: 5px;margin-bottom: 10px; }
    .nav-pills>li>a {padding: 5px 10px;}

    .ad { padding: 5px;background: #F5F5F5;color: #222;font-size: 80%;border: 1px solid #E5E5E5; }
    .ad a.title {color: #15C;text-decoration: none;font-weight: bold;font-size: 110%;}
    .ad a.url {color: #093;text-decoration: none;}
</style>
<body>
<div class="container bootstrap snippets bootdey">
    <div class="row">
        <div class="col-sm-3 col-md-2">
            <div class="btn-group">
                <button type="button" class="btn btn-info dropdown-toggle" data-toggle="dropdown">
                    Mail <span class="caret"></span>
                </button>
                <ul class="dropdown-menu" role="menu">
                    <li><a href="#">Mail</a></li>
                    <li><a href="#">Contacts</a></li>
                    <li><a href="#">Tasks</a></li>
                </ul>
                
            </div>
            
        </div>
        <p>Welcome, <?=$_SESSION["mail_mail"];?></p>
        <a href="logout.php">logout</a>
    </div> 
    <hr>
    <div class="row">
        <div class="col-sm-3 col-md-2">
            <hr>
            <ul class="nav nav-pills nav-stacked">
                <li class="active"><a href="#"><span class="badge pull-right"><?=$res->num_rows?></span> Inbox </a>
                </li>
            </ul>
        </div>
        <div class="col-sm-9 col-md-10">
            <!-- Nav tabs -->
            <ul class="nav nav-tabs">
                <li class="active"><a href="#home" data-toggle="tab"><span class="glyphicon glyphicon-inbox">
                </span>Primary</a></li>
                </a></li>
            </ul>
            <!-- Tab panes -->
            <div class="tab-content">
                <div class="tab-pane fade in active" id="home">
                    <div class="list-group">
                        <?php while($email=$res->fetch_assoc()){?>
                        <a href="mail_view.php?id=<?=$email['id']?>" class="list-group-item">
                            <span class="glyphicon glyphicon-star-empty"></span><span class="name label label-info" style="min-width: 120px;
                                display: inline-block;">Ghazy Corp</span> <span class=""><?=substr($email['content'],0,20)?></span>
                            <span class="text-muted" style="font-size: 11px;">- More content here</span> <span class="pull-right">
                            </span></span>
                        </a>
                        <?php }?>
                    </div>
                </div>
                <div class="tab-pane fade in" id="profile">
                    <div class="list-group">
                        <div class="list-group-item">
                            <span class="text-center">This tab is empty.</span>
                        </div>
                    </div>
                </div>
                <div class="tab-pane fade in" id="messages">
                    ...</div>
                <div class="tab-pane fade in" id="settings">
                    This tab is empty.</div>
            </div>
        </div>
    </div>
</div>
</body>
</html>