<?php session_start(); ?>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Blog</title>
    <link rel="stylesheet" href="/style.css">
    <?php include 'theme.php'; ?>
  </head>

  <body>
    <h1>welcome to my blog! 🍊</h1>
    <p>a place for me to talk about stuff</p>
    <p>
      switch color theme:
      <a href="/set.php?theme=dark">dark mode</a>
      <a href="/set.php?theme=light">light mode</a>
    </p>
    <hr>
    <ul>
      <?php
        $posts = glob("posts/*");
        foreach ($posts as $post) {
          $name = basename($post);
          echo '<li><a href="/post.php?post=' . $name . '">' . $name . '</a></li>';
        }
      ?>
    </ul>
  </body>
</html>
