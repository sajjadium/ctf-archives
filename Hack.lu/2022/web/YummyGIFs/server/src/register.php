<?php
include_once('include/php_head.php');

if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] === true) {
  header('Location: /');
  exit();
}

$usernameregex = '/^\w+$/';
$passwordlength = 8;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  if ($_POST['csrf'] === $_SESSION['csrf']) {
    if (is_string($_POST['username']) && is_string($_POST['password'])) {
      if (preg_match_all($usernameregex, $_POST['username']) === 1 && strlen($_POST['password']) >= $passwordlength) {
        try {
          DB::register($_POST['username'], $_POST['password']);
          $success = 'Success. Login to start uploading yummy GIFs! 🥳';
        } catch (Exception $e) {
          $error = $e->getMessage();
        }
      } else {
        $error = 'Wrong username or password format';
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
    <h2>Register</h2>
    <form method="post">
      <input name="csrf" type="hidden" value="<?= e($_SESSION['csrf']) ?>">
      <label for="username">Username</label>
      <input name="username" required placeholder="\w+" pattern="\w+">
      <label for="password">Password</label>
      <input name="password" required placeholder=".{8,}" minlength="8" type="password">
      <input type="submit" value="Register">
    </form>
  </main>
  <?php include('include/footer.php') ?>
</body>

</html>