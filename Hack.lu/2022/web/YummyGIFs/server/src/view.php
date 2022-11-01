<?php
include_once "include/php_head.php";

if (isset($_GET['id']) && is_string($_GET['id'])) {
  try {
    $gif = DB::getGIFById($_GET['id']);
    $title = $gif['title'];
    $description = $gif['description'];
    $path = '/uploads/' . $gif['random_id'] . '/' . $gif['name'];
  } catch (Exception $e) {
    $not_found = $e->getMessage();
  }
} else {
  $not_found = 'GIF not found';
}

if (isset($not_found) && $not_found) {
  header('HTTP/1.1 404 Not Found');
}

?>

<!DOCTYPE html>
<html>
<?php include('include/head.php') ?>

<body>
  <?php include('include/header.php') ?>
  <main class="container">
    <?php if (isset($not_found) && $not_found) : ?>
      <article>
        <h1><?= e($not_found) ?></h1>
      </article>
    <?php else : ?>
      <article>
        <header><h4 class="image-title"><?= s($title) ?></h4></header>
        <a href="<?= e($path) ?>" target="_blank">
          <img class="view-image" src="<?= e($path) ?>" title="<?= e($gif['name']) ?>">
        </a>
        <footer><?= s($description) ?></footer>
      </article>
    <?php endif ?>
  </main>
  <?php include('include/footer.php') ?>
</body>

</html>