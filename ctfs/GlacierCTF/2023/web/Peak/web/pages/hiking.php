<!DOCTYPE html>
<html lang="en">
    <?php 
        include_once "../includes/header.php";
        include_once "../includes/csp.php";
    ?>
    <head>
    <style>
        body {
            height: 100vh;
            display: flex;
        }
        #trails {
            background-image: url('/assets/img/map.png');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            width: 100%;
            height: 100%;
        }
    </style>
    </head>
    <body>
        <?php include_once "../includes/menu.php"; ?>

        <header class="hero bg-primary text-white text-center py-5">
    <div class="container">
        <h1>Großglockner Hiking Trails</h1>
        <p>Discover the Beauty of Alpine Hiking</p>
    </div>
</header>
<section id="trails" class="bg-light d-flex align-items-center py-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-6">
                <div class="rounded p-4" style="background-color: rgba(255, 255, 255, 0.7);">
                    <h2 class="text-center">Top 4 Trails</h2>
                    <div class="row">
                        <div class="col-md-6">
                            <div class="card mb-4">
                                <div class="card-body">
                                    <h5 class="card-title">Trail 1: Summit Ascent</h5>
                                    <p class="card-text">
                                        <strong>Duration:</strong> 6 hours<br>
                                        <strong>Length:</strong> 12 km<br>
                                        <strong>Elevation Gain:</strong> 1,200 meters<br>
                                    </p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="card mb-4">
                                <div class="card-body">
                                    <h5 class="card-title">Trail 2: Glacier Exploration</h5>
                                    <p class="card-text">
                                        <strong>Duration:</strong> 4 hours<br>
                                        <strong>Length:</strong> 8 km<br>
                                        <strong>Elevation Gain:</strong> 800 meters<br>
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-6">
                            <div class="card mb-4">
                                <div class="card-body">
                                    <h5 class="card-title">Trail 3: Valley Loop</h5>
                                    <p class="card-text">
                                        <strong>Duration:</strong> 3 hours<br>
                                        <strong>Length:</strong> 6 km<br>
                                        <strong>Elevation Gain:</strong> 400 meters<br>
                                    </p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="card mb-4">
                                <div class="card-body">
                                    <h5 class="card-title">Trail 4: Alpine Meadows</h5>
                                    <p class="card-text">
                                        <strong>Duration:</strong> 5 hours<br>
                                        <strong>Length:</strong> 10 km<br>
                                        <strong>Elevation Gain:</strong> 600 meters<br>
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
</body>
<?php include "../includes/footer.php"?>
</html>