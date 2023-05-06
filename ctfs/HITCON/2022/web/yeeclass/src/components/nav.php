<nav>
    <a href="index.php">[Home]</a><?php if (isset($_SESSION["userid"])) { ?> | <a href="submission.php">[My Submissions]</a> <?php } ?>
    <div class="right">
    <?php if (!isset($_SESSION["userid"])) { ?>
        <form action="index.php" method="POST">
            <input type="text" name="username" id="username" placeholder="Username" pattern="^\w{6,20}$" autocomplete="off">
            <input type="password" name="password" id="password" placeholder="Password" autocomplete="off">
            <input type="submit" value="Login/Register">
        </form>
    <?php } else { ?>
        <span>Hi, <?= $_SESSION["username"] ?></span>
        <a href="index.php?logout">[Logout]</a>
    <?php } ?>
    </div>
</nav>