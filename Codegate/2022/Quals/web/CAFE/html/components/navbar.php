<nav class="navbar navbar-expand-md navbar-dark" style="background-color: #292626; heigth:18%;">
    <div class="container">
        <a class="navbar-brand" href="/">
            <p style=" margin-top: -5px;">CAFE</p>
        </a>
        <button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbar2SupportedContent">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse text-center justify-content-end" id="navbar2SupportedContent">
            <ul class="navbar-nav" style="font-size: 18px;">
                <?php if(!isset($_SESSION['id'])) { ?>
                    <li class="nav-item"><a class="nav-link" href="/login">Login</a></li>
                    <li class="nav-item"><a class="nav-link" href="/register">Register</a></li>
                <?php } else { ?>
                    <li class="nav-item"><a class="nav-link" href="/write">Write</a></li>
                    <li class="nav-item"><a class="nav-link" href="/logout">Logout</a></li>
                <?php } ?>
            </ul>
        </div>
    </div>
</nav>