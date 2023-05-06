<!DOCTYPE html>
<html lang="en">
   <head>
   <!-- Basic -->
   <meta charset="utf-8">
   <meta http-equiv="X-UA-Compatible" content="IE=edge">
   <!-- Mobile Metas -->
   <meta name="viewport" content="width=device-width, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no">
   <!-- Site Metas -->
   <title>Christmas Wishes</title>
   <meta name="keywords" content="">
   <meta name="description" content="">
   <meta name="author" content="">
   <!-- Site Icons -->
   <link rel="shortcut icon" href="imgs/fevicon.png" type="image/x-icon" />
   <!-- Bootstrap CSS -->
   <link rel="stylesheet" href="css/bootstrap.min.css">
   <!-- Site CSS -->
   <link rel="stylesheet" href="style.css">
   <!-- Colors CSS -->
   <link rel="stylesheet" href="css/colors.css">
   <!-- ALL VERSION CSS -->
   <link rel="stylesheet" href="css/versions.css">
   <!-- Responsive CSS -->
   <link rel="stylesheet" href="css/responsive.css">
   <!-- Custom CSS -->
   <link rel="stylesheet" href="css/custom.css">
   <!-- Modernizer for Portfolio -->
   <script src="js/modernizer.js"></script>
   <!--[if lt IE 9]>
   <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
   <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
   <![endif]-->
   </head>
   <body class="christmas_version">

      <div id="preloader">
         <img class="preloader" src="imgs/loading.gif" alt="">
      </div>

      <div id="home" class="section first-section wb banner_section">
         <div class="container">
            <div class="row">
               <div class="col-md-7">
                    <div class="contact_form">
                        <h3><i class="fa fa-envelope-o"></i> Your Wishes</h3>
                        <form id="contactform1" class="row" name="contactform" method="post">
                            <fieldset class="row-fluid">
                                <div class="col-lg-12">
									<div style="color: #000000">
										在这里写下你的圣诞愿望吧！愿望箱会将你的愿望转交给圣诞FUMO！<br>
										Write down your Christmas wishes here! <br>
										The wish box will forward your wishes to Santa FUMO!<br>
										现已全面支持JSON！<br>
										Now fully supports submitting your wishes using JSON data!<br>
									</div>
                                   <textarea class="form-control" name="wishes" id="comments" rows="6" placeholder='wishes'>{"/etc/passwd":"FUMO can give you as a gift the files represented by the key values~"}</textarea>
                                </div>
                                <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12 text-center">
                                    <button type="submit" value="SEND" id="submit1" class="btn btn-light btn-radius btn-brd grd1 btn-block">Send</button>
                                </div>
                                <div class="col-lg-12 right">
									<div>
                                        Or... just look at <a href="/test.php">PHPINFO()</a>?
									</div>
                                </div>
                            </fieldset>
                        </form>
                    </div>
                </div>
            </div>
            <!-- end row -->
         </div>
         <!-- end container -->
      </div>

      <script src="js/all.js"></script>
      <script src="js/custom.js"></script>
   </body>
</html>
<?php
if (isset($_POST['wishes'])) {
    echo "Your wishes is".var_export($_POST['wishes']);

    $data = jsonparser($_POST['wishes']);

    echo "Santa FUMO heard your wishes is ".$data;
    readfile($data);
}