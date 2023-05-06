<?php include('private/verify_login.php');?>
<?php
try{
    $sql = new MySQLobject();
    $data = $sql->get_data($name);
}catch(Exception $e){
    die('{"error":"Something went wrong while fetching your data!"}');
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
<body class="container-fluid p-0">
    <?php include('assets/navbar_registered.php'); ?>
    
    <div class="row container-fluid justify-content-center mt-4">
        <div class="col-8 text-center mt-4">
            <h1 class="display-3">Your Profile</h1>
        </div>
    </div>
    
        <div class="row justify-content-center container-fluid mt-5 text-center">
        <div class="col-2 p-4 border border-danger border-right-0 border-top-0 my-3">
            <h3 class="fs-2">Username</h3>
        </div>
        <div class="col-4 border border-primary roundend p-4 border-top-0 border-right-0 my-3">
            <p class="fs-4 font-monospace"><?php echo htmlentities($data["username"], ENT_QUOTES, 'UTF-8');?></p>
        </div>

        <div class="w-100"></div>
    
        <div class="col-2 p-4 border border-danger border-right-0 border-top-0 my-3">
            <h3 class="fs-2">Email</h3>
        </div>
        <div class="col-4 border border-primary roundend p-4 border-top-0 border-right-0 my-3">
            <p class="fs-4 font-monospace"><?php echo htmlentities($data["email"], ENT_QUOTES, 'UTF-8');?></p>
        </div>

        <div class="w-100"></div>

        <div class="col-2 p-4 border border-danger border-right-0 border-top-0 my-3">
            <h3 class="fs-2">Description</h3>
        </div>
        <div class="col-4 border border-primary roundend p-4 border-top-0 border-right-0 my-3">
            <p class="fs-4 font-monospace"><?php echo $data["description"];?></p>
        </div>
    </div>
    <div class="row justify-content-center">
        <div class="col text-end mt-2">
            <form action="/description.php" method='GET'>
                <input type="hidden" name="name" value=<?php echo '"'.$name.'"';?>></input>
                <button class="btn btn-secondary" type="submit">Change Description!</button>
            </form>
        </div>
        <div class="col text-left mt-2">
            <form action="/report.php" method='GET'>
                <input type="hidden" name="name" value=<?php echo '"'.$name.'"';?>></input>
                <button class="btn btn-danger" type="submit">Report color to an admin!</button>
            </form>
        </div>
    </div>
    
</body>
</html>