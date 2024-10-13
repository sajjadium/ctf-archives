<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/static/bootstrap/dist/css/bootstrap.css">
    <title><?= $title; ?></title>
</head>

<body data-bs-theme="white">
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">SerenityPDF</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarScroll" aria-controls="navbarScroll" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarScroll">
                <ul class="navbar-nav me-auto my-2 my-lg-0 navbar-nav-scroll" style="--bs-scroll-height: 100px;">
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="/pdf-maker">PDF Maker</a>
                    </li>
                </ul>
            </div>
            <form class="d-flex grid gap-3" role="search">
                <?php
                if (session()->get("username")) {
                ?>
                    <div class="btn bt-outline-primary nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            User
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="/info">info</a></li>
                            <?php
                            if (session()->get("role") === "admin") {
                            ?>
                                <li><a class="dropdown-item" href="/admin">admin</a></li>
                            <?php
                            }
                            ?>
                        </ul>
                    </div>
                <?php
                }
                ?>
                <a class="btn btn-outline-success" href="/register">Register</a>
                <a class="btn btn-outline-primary" href="/login">Login</a>
            </form>
        </div>
    </nav>