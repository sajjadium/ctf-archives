<?php
  session_start();

  if (isset($_GET['post']) && file_exists($post = 'posts/' . $_GET['post'])) {
    $ok = true;
  } else {
    $ok = false;
    http_response_code(404);
  }
?>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= htmlentities($_GET['post']) ?></title>
    <link rel="stylesheet" href="/style.css">
    <?php include 'theme.php'; ?>
  </head>

  <body>
    <?php
      if ($ok) {
        echo '<h1>' . htmlentities($_GET['post']) . '</h1><hr><div class="post">';
        include $post;
        echo '</div>';
      } else {
        echo '<h1>post not found :(</h1><hr>';
      }
    ?>
    <a href="/">home</a>
  </body>
</html>
