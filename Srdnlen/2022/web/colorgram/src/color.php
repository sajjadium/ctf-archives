<?php
require_once('private/verify_login.php');
require_once('private/filters.php');

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <meta http-equiv="Content-Security-Policy" content="default-src 'unsafe-inline'; connect-src 'none'; object-src 'none';">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ColorGram</title>
</head>

<?php
    if(isset($_GET['color'])){
        $color = validate_color($_GET['color']);
        echo '<body class=container-fluid style=height:100vh;background-color:'.$color.'><div class="row justify-content-center" style="height:100vh;">
        <div class="col-12 align-self-center text-center">
            <h1>Here is your color, click <a href="/account.php?name='.$name.'">here</a> to go back</h1>
        </div>
    </div>';
    }else{
        echo '<body class=container-fluid style=height:100vh;>';
        echo '<div class="row justify-content-center text-center m-5">
        <div class="col-7">
            <h2>Insert your color</h2>
        </div>
        <div class="col-7">
            <input type="text" name="color" id="color"></input>
            <button type="submit" onclick="change_page()">Change!</button>
        </div>
    </div>
    <script>
        function change_page(){
            var color = document.getElementById("color").value;
            window.location= window.location+"&color="+color;
        }
    </script>';
    }
?>
</body>
</html>