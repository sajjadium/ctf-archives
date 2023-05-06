<?php 
require_once('private/verify_login.php');
require_once('private/mysql.php');
require_once('private/filters.php');

if(isset($_POST['description'])){
    $mysql = new MySQLobject();
    $description = validate_description($_POST['description']);
    try{
        $mysql->change_description($name,urldecode($description));
    }catch(Exception $e){
        echo $e;
        die('{"error":"Couldnt change your description"}');
    }
    header('Location: http://'.$_SERVER['HTTP_HOST'].'/account.php?name='.$name);
    die('{"Success":"Description Changed!"}');
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <meta http-equiv="Content-Security-Policy" content="default-src 'self' data: *; connect-src 'self'; object-src 'none';">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ColorGram</title>
</head>
<body class="container-fluid">
    <div class="row justify-content-center text-center m-5">
        <div class="col-7">
            <h2>Change Description!</h2>
        </div>
        <div class="col-7">
            <form action=<?php echo '"/description.php?name='.$name.'"'; ?> method='POST'>
                <input type="text" name="description" id="description"></input>
                <button type="submit">Change!</button>
            </form>
            
        </div>
    </div>
</body>
</html>