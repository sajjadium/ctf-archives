<nav class="container-fluid">
  <ul>
    <li><a href="/"><b>Yummy</b>GIFs</a></li>
  </ul>
  <ul>
    <?php if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] === true) : ?>
      <li>
        Welcome back <?= e($_SESSION['username']) ?>!
      </li>
      <li>
        <a href="/report.php">Report GIF</a>
      </li>
      <li>
        <form class="inline-form" action="/logout.php" method='post'>
          <input name="csrf" type="hidden" value="<?= e($_SESSION['csrf']) ?>">
          <input role="button" type="submit" value="Logout">
        </form>
      </li>
    <?php else : ?>
      <li><a href="/register.php">Register</a></li>
      <li>
        <form class="inline-form" action="/login.php" method="get">
          <input role="button" type="submit" value="Login">
        </form>
      </li>
    <?php endif ?>
  </ul>
</nav>