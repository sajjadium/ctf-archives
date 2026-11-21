<?php
    include_once "includes/session.php";
?>
<!DOCTYPE html>
<html lang="en">
    <?php 
        include_once "includes/header.php";
        include_once "includes/csp.php";
    ?>
    <body>
        <?php include_once "includes/menu.php"; ?>


<header class="hero bg-primary text-white text-center py-5">
    <div class="container">
        <h1>Welcome to the Großglockner</h1>
        <p>Your Gateway to Adventure and Beauty</p>
    </div>
</header>

<section id="welcome" class="py-5" style="background-image: url('/assets/img/hiking.png'); background-size: cover;">
    <div class="container h-100">
        <div class="row h-100 justify-content-center align-items-center">
            <div class="col-lg-6">
                <div class="rounded p-4" style="background-color: rgba(255, 255, 255, 0.7);">
                    <h2>Welcome to the Großglockner</h2>
                    <p>
                        Welcome to the majestic Großglockner, Austria's highest peak, standing tall at 3,798 meters (12,461 feet) above sea level. Nestled within the breathtaking landscapes of the Hohe Tauern National Park, this iconic Alpine destination beckons adventurers, nature lovers, and history enthusiasts alike. The Großglockner offers not only panoramic views of surrounding peaks and valleys but also the opportunity to explore its glaciers, including the renowned Pasterze Glacier. Whether you're an avid climber seeking a challenge or a traveler in search of alpine beauty, the Großglockner has something extraordinary to offer.
                    </p>
                </div>
            </div>
        </div>
    </div>
</section>
<section id="activities" class="bg-light py-5">
    <div class="container">
        <h2>Activities</h2>
        <div class="row centered">
            <div class="col-md-4">
                <a href="/pages/hiking.php">
                    <div class="card">
                        <img src="/assets/img/map.png" class="card-img-top" alt="Hiking">
                        <div class="card-body">
                            <h5 class="card-title">Hiking Adventures</h5>
                            <p class="card-text">Explore scenic trails and breathtaking vistas.</p>
                        </div>
                    </div>
                </a>
            </div>
            <div class="col-md-4">
                <a href="/pages/climbing.php">
                    <div class="card">
                        <img src="/assets/img/climbing.png" class="card-img-top" alt="Climbing">
                        <div class="card-body">
                            <h5 class="card-title">Mountain Climbing</h5>
                            <p class="card-text">Challenge yourself with thrilling ascents.</p>
                        </div>
                    </div>
                </a>
            </div>
            <div class="col-md-4">
                <div class="card">
                    <a href="/pages/sightseeing.php">
                        <img src="/assets/img/sightseeing.png" class="card-img-top" alt="Sightseeing">
                        <div class="card-body">
                            <h5 class="card-title">Sightseeing Tours</h5>
                            <p class="card-text">Discover the beauty of the Alps with guided tours.</p>
                        </div>
                    </a>
                </div>
            </div>
        </div>
    </div>
</section>
</body>
<?php include "./includes/footer.php"?>
</html>