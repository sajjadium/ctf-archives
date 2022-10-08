<nav class="navbar navbar-expand-lg navbar-light bg-danger py-4">
    <div class="container-fluid">
        <a class="navbar-brand text-light" href=<?php echo '"/account.php?name='.$name.'"';?>>
            <p class="mx-4 p-3 display-3 fst-italic fw-bold">COLORGRAM</p>
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-end mx-4" id="navbarNavAltMarkup">
            <div class="navbar-nav">
                <a <?php if($_SERVER['PHP_SELF'] == '/register.php'){echo 'class="nav-link fs-4 fw-bold mx-2 active" aria-current="page"';}else{ echo 'class="nav-link fs-4 fw-bold mx-2"';}?> href="/register.php">Register</a>
                <a <?php if($_SERVER['PHP_SELF'] == '/login.php'){echo 'class="nav-link fs-4 fw-bold mx-2 active" aria-current="page"';}else{ echo 'class="nav-link fs-4 fw-bold mx-2"';}?> href="/login.php">Login</a>
            </div>
        </div>
    </div>
</nav>