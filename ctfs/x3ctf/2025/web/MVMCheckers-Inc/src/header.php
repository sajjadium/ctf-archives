<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SpellCheckers Inc.</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <link href="style.css" rel="stylesheet"/>
</head>
<body>

<nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">SpellCheckers Inc.</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link active" aria-current="page" href="/">Home</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/magicians.php">Magicians</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/administration.php">Magician Administration</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/rebuild?page=booking.json">Booking</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/rebuild?page=about.json">About</a>
                </li>
            </ul>
        </div>
    </div>
</nav>
<div class="container my-8">
<?php
putenv("HOME=/home/app");
?>
