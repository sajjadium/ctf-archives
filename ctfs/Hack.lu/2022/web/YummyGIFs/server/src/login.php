<?php
include_once('include/php_head.php');

if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] === true) {
  header('Location: /');
  exit();
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  if ($_POST['csrf'] === $_SESSION['csrf']) {
    if (is_string($_POST['username']) && is_string($_POST['password'])) {
      try {
        $userinfo = DB::login($_POST['username'], $_POST['password']);
        $_SESSION['loggedin'] = true;
        $_SESSION['username'] = $userinfo['username'];
        $_SESSION['user_id'] = $userinfo['user_id'];

        header('Location: / ');
        exit();
      } catch (Exception $e) {
        $error = $e->getMessage();
      }
    } else {
      $error = 'Sussy input 🤨';
    }
  } else {
    $error = $csrf_error;
  }
}
?>
<!DOCTYPE html>
<html>
<?php include('include/head.php') ?>

<body>
  <?php include('include/header.php') ?>
  <main class="container">
    <h2>Login</h2>
    <form method="post">
      <input name="csrf" type="hidden" value="<?= e($_SESSION['csrf']) ?>">
      <label for="username">Username</label>
      <input id="username" name="username" required>
      <label for="password">Password</label>
      <input id="password" name="password" required type="password">
      <input id="submit" type="submit" value="Login">
    </form>
  </main>
  <?php include('include/footer.php') ?>
</body>

</html>