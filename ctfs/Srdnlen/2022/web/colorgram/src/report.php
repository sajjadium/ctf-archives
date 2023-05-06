<?php 
require_once('private/verify_login.php');
require_once('private/filters.php');

if(isset($_POST['admin_request'])){
    $req = validate_report($_POST['admin_request']);
    try{
        $req = file_get_contents(getenv('URL_BOT').'?color='.$req);
    }catch(Exception $e){
        die('{"error":"Couldnt report to admin!"}');
    }
    header('Location: http://'.$_SERVER['HTTP_HOST'].'/account.php?name='.$name);
    die('{"Success":"Report sent!"}');
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
            <h2>Report to Admin!</h2>
        </div>
        <div class="col-7">
            <form action=<?php echo '"/report.php?name='.$name.'"'; ?> method='POST'>
                <input type="text" name="admin_request" id="admin_request"></input>
                <button type="submit">Report!</button>
            </form>
            
        </div>
    </div>
</body>
</html>