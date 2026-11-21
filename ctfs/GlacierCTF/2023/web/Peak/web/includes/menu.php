<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
        <a class="navbar-brand" href="/">Großglockner</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav mr-auto">
                <li class="nav-item">
                    <a class="nav-link" href="/pages/directions.php">
                        Directions
                    </a>
                </li>
                <?php if(isset($_SESSION['user']) && $_SESSION['user']['role'] == "admin") : ?>
                <li class="'nav-item"><a class="nav-link" href="/admin/map.php">Edit map</a></li>
                <?php else:?>
                    <li class="nav-item">
                    <a class="nav-link" href="/pages/contact.php">
                        Contact Us
                    </a>
                </li>
                <?php endif; ?>
            </ul>
            <?php if(isset($_SESSION['user'])) : ?>
                <ul class="navbar-nav ms-auto align-items-baseline">
                    <li class="nav-item dropdown">
                        <a id="settingsDropdown" class="nav-link" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <?php echo htmlentities($_SESSION['user']['username']); ?>
                            <svg class="ms-2" width="18" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M10 3a1 1 0 01.707.293l3 3a1 1 0 01-1.414 1.414L10 5.414 7.707 7.707a1 1 0 01-1.414-1.414l3-3A1 1 0 0110 3zm-3.707 9.293a1 1 0 011.414 0L10 14.586l2.293-2.293a1 1 0 011.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                            </svg>
                        </a>
                        <div class="dropdown-menu dropdown-menu-end animate__slideIn" aria-labelledby="settingsDropdown">
                            <a class="dropdown-item px-4" href="/actions/logout.php" onclick="event.preventDefault(); document.getElementById('logout-form').submit();">Log out</a>
                            <form method="POST" id="logout-form" action="/actions/logout.php">
                                <input type="hidden" value="logout" name="logout">
                            </form>
                        </div>
                    </li>
                </ul>
          <?php else : ?>
            <ul class="navbar-nav ms-auto align-items-baseline">
                <li class="nav-item dropdown">
                    <a class="nav-link" href="/login.php">
                        Login/Register
                    </a>
              </li>
          </ul>
          <?php endif; ?>
        </div>
    </div>
</nav>