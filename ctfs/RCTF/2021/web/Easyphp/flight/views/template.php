<!DOCTYPE html>
<html>

<head>
    <?= $head_content ?>
</head>

<body>
    <div class="container">

        <header class="d-flex flex-wrap align-items-center justify-content-center justify-content-md-between py-3 mb-4 border-bottom">
            <a href="/" class="d-flex align-items-center col-md-3 mb-2 mb-md-0 text-dark text-decoration-none">
                <svg class="bi me-2" width="40" height="32" role="img" aria-label="Bootstrap">
                    <use xlink:href="#bootstrap"></use>
                </svg>
            </a>

            <ul class="nav col-12 col-md-auto mb-2 justify-content-center mb-md-0">
                <li><a href="/" class="nav-link px-2 link-dark">Home</a></li>
                <li><a href="/admin" class="nav-link px-2 link-dark">File Explore</a></li>

            </ul>

            <div class="col-md-3 text-end">
                <?php
                if ($_SESSION["user"]) {

                ?>
                    Hello,<?= $_SESSION["user"] ?>
                <?php
                } else {
                ?>
                    <button onclick="document.location='/login'" type="button" class="btn btn-outline-primary me-2">Login</button>
                <?php
                }
                ?>

            </div>
        </header>
        <?= $body_content ?>
    </div>

</body>

</html>