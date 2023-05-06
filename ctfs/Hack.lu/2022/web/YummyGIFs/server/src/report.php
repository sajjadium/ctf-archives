<?php
include_once('include/php_head.php');

if (!isset($_SESSION['loggedin']) || $_SESSION['loggedin'] !== true) {
  header('Location: /login.php');
  exit();
}

?>

<!DOCTYPE html>
<html>
<?php include('include/head.php') ?>

<body>
  <?php include('include/header.php') ?>
  <main class="container">
    <h2>Report GIF</h2>
    <p>Report a GIF URL that violates our <a href="/tos.php">TOS</a>. Don't report GIFs from other sites!</p>
    <form id="report-form" action="/submitreport" method="post">
      <label for="link">Report URL</label>
      <input name="link" required>
      <button class="g-recaptcha" data-sitekey="<?= e(getenv("RECAPTCHA_PUBLIC_KEY")) ?>" data-callback="onSubmit" data-action="submit">Send report</button>
    </form>
  </main>
  <?php include('include/footer.php') ?>
  <script src="/static/report.js"></script>
  <script src="https://www.google.com/recaptcha/api.js" async defer></script>
</body>

</html>