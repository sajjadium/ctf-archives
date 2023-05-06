<?php
require_once('config.php');
if(!isset($_SESSION["username"])){
    header("Location: login.php");
    die();
}

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link rel="shortcut icon" href="assets/images/favicon.ico" type="image/x-icon">
    <title>ASTLIBRA!</title>

    <!-- Vendor css -->
    <link rel="stylesheet" href="./src/vendors/@mdi/font/css/materialdesignicons.min.css">

    <!-- Base css with customised bootstrap included -->
    <link rel="stylesheet" href="./src/css/miri-ui-kit-free.css">

    <!-- Stylesheet for demo page specific css -->
    <link rel="stylesheet" href="./assets/css/demo.css">
    <script>
        function visit(){
            var result = "<h1>Loading...</h1>";
            document.getElementsByName("view_panel")[0].srcdoc = result;
            document.getElementsByName("source_code")[0].innerText = result;
            var url = document.getElementsByName("URL")[0].value;
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/api.php", true);
            xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            xhr.onload = function (e) {
                if (xhr.readyState === 4) {
                    if (xhr.status === 200) {
                        result = JSON.parse(xhr.responseText);
                        if(result.status == "success"){
                            document.getElementsByName("view_panel")[0].srcdoc = atob(result.message);
                            document.getElementsByName("source_code")[0].innerText = atob(result.message);
                        }
                    } else {
                        document.getElementsByName("view_panel")[0].srcdoc = xhr.statusText + " error";
                        document.getElementsByName("source_code")[0].innerText = xhr.statusText + " error";
                    }
               } else {
                    document.getElementsByName("view_panel")[0].srcdoc = "something error";
                    document.getElementsByName("source_code")[0].innerText = "something error";
               }
            };
            xhr.onerror = function (e) {
                document.getElementsByName("view_panel")[0].srcdoc = "something error";
                document.getElementsByName("source_code")[0].innerText = "something error";
            };
            xhr.send("URL=" + url);  
        }
    </script>
</head>
<body class="bg-dark">
    <header class="miri-ui-kit-header">
        <nav class="navbar navbar-expand-lg navbar-dark bg-transparent fixed-on-scroll">
            <div class="container">
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#miriUiKitNavbar"
                    aria-controls="navbarSupportedContent2" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="mdi mdi-menu"></span>
                </button>
            
                <div class="collapse navbar-collapse" id="miriUiKitNavbar">
                    <div class="navbar-nav ml-auto">
                      

                        <li class="nav-item dropdown">
                            <a href="#" class="nav-link dropdown-toggle" data-toggle="dropdown">
                                <?php echo $_SESSION["username"]; ?>
                            </a>
                            <div class="dropdown-menu dropdown-menu-right ">
                                <a href="logout.php" class="dropdown-item"><i class="dropdown-item-icon mdi mdi-lock-outline"></i>Logout</a>
                            </div>
                        </li>
                    </div>
                </div>
            </div>
        </nav>
        <div class="miri-ui-kit-header-content text-center text-white d-flex flex-column justify-content-center align-items-center">
            <div class="form-group col-md-3">
                <label for="iconRightInput" class="sr-only">Input with right icon</label>
                <div class="input-group input-group-pill">
                    <input type="text" class="form-control outline-success" id="iconRightInput" name="URL" placeholder="https://..." value="https://store.steampowered.com/app/1718570/ASTLIBRA_Revision/">
                    <div class="input-group-append">
                        <span class="mdi mdi-star-circle input-group-text"></span>
                    </div>
                </div>
            </div>
            <p class="py-3"><a href="#home3" onclick="visit()" class="btn btn-dark mr-3">Explore</a></p>

        </div>
    </header>
    <div class="container content-wrapper" id="demo-content">
        <div class="card card-demo-wrapper">
            <div class="card-body mb-4">
                
                <div class="col-lg-6 grid-margin">
                    <h6 class="pb-3" class="mb-3">Results</h6>
                    <ul class="nav nav-pills nav-pills-icon-text" id="myTab" role="tablist">
                        <li class="nav-item">
                            <a class="nav-link active" id="home-tab3" data-toggle="tab" href="#home3" role="tab" aria-controls="home3"
                                aria-selected="true"><i class="mdi mdi-home"></i>Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" id="coupon-tab3" data-toggle="tab" href="#coupon3" role="tab" aria-controls="coupon3"
                                aria-selected="false"><i class="mdi mdi-receipt"></i>View Source</a>
                        </li>
                    </ul>
                    <div class="tab-content mb-5" id="myTabContent3">
                        <div class="tab-pane fade show active" id="home3" role="tabpanel" aria-labelledby="home-tab3" style="position: relative; width: 100%; 
    padding-top: calc(100% * 720 / 1280);">
                             <iframe srcdoc="None" name="view_panel"  style="position: absolute; width: 100%; height: 100%; top: 0;">

                             </iframe>
                        </div>
                        <div class="tab-pane fade" id="coupon3" role="tabpanel" aria-labelledby="coupon-tab3">
                            <code name="source_code"> 
                               
                            </code>
                        </div>
                    </div>
                </div>
                
            </div>
        </div>
    </div>
    <footer>
        <div class="container">
           
            <nav class="navbar navbar-dark bg-transparent navbar-expand d-block d-sm-flex text-center">
                <span class="navbar-text">&copy; BootstrapDash. All rights reserved.</span>
                <div class="navbar-nav ml-auto justify-content-center">
                    <a href="#" class="nav-link">Support</a>
                    <a href="#" class="nav-link">Terms</a>
                    <a href="#" class="nav-link">Privacy</a>
                </div>
            </nav>
        </div>
    </footer>
    <script src="./src/vendors/jquery/dist/jquery.min.js"></script>
    <script src="./src/vendors/popper.js/dist/umd/popper.min.js"></script>
    <script src="./src/vendors/bootstrap/dist/js/bootstrap.min.js"></script>
    <script src="./src/js/miri-ui-kit.js"></script>
</body>
</html>