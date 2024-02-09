<?php
session_start();
require_once("db.php");
if(!isset($_SESSION['user_id']))
{
    die("<script>window.location.href='index.php';</script>");
}


if ($_SESSION["role"]!=="admin")
{
    die("You are not admin,hahaha<br><a href='logout.php'>Click Here</a> to logout");
}

$stmt = $conn->prepare("select * from users");
$stmt->execute();
$res=$stmt->get_result();


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
<body>
<table class="table">
<thead>
    <tr>
    <th scope="col">#</th>
    <th scope="col">email</th>
    <th scope="col">photo</th>
    </tr>
</thead>
<tbody>
<?php $count=0;while ($user=$res->fetch_assoc()){?>
    <tr>
    <th scope="row"><?=++$count;?></th>
    <td><?=$user["email"]?></td>
    <td><a href="user_photo.php?id=<?=$user['id']?>">Click Here to view user photo</a></td>
    </tr>
    <?php }?>
    </tbody>
</table>
</body>
</html>


