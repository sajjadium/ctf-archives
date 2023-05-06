<?php
include_once('include/php_head.php');

if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] === true && isset($_SESSION['user_id'])) {
  try {
    $res = DB::getGIFsByUser($_SESSION['user_id']);
    $res = $res->fetch_all(MYSQLI_ASSOC);
    $gifs = array_filter($res, function ($gif) {
      return file_exists(__DIR__ . '/uploads/' . $gif['random_id'] . '/' . $gif['name']);
    });
  } catch (Exception $e) {
    $error = 'Database error';
  }
}

?>
<!DOCTYPE html>
<html>
<?php include('include/head.php') ?>

<body>
  <?php include('include/header.php') ?>
  <main class="container">
    <?php if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] === true) : ?>
      <section>
        <hgroup>
          <h2>Your YummyGIFs</h2>
          <h3>Share them everywhere 🌍</h3>
        </hgroup>
        <div class="image-gallery">
          <?php foreach ($gifs as $gif) : ?>
            <article>
              <header>
                <h4 class="image-title">
                  <a href="/view.php?id=<?= e($gif['random_id']) ?>"><?= s($gif['title']) ?></a>
                </h4>
              </header>
              <div>
                <a href="/view.php?id=<?= e($gif['random_id']) ?>">
                  <img src="/uploads/<?= e($gif['random_id']) ?>/<?= e($gif['name']) ?>" title="<?= e($gif['name']) ?>">
                </a>
              </div>
            </article>
          <?php endforeach ?>
        </div>
      </section>
      <section>
        <hgroup>
          <h2>Upload a new GIF</h2>
          <h4>
            Only valid and yummy GIF files are allowed. Max filesize 2MB. No GIFs that violate our <a href="/tos.php">TOS</a>.<br>
            <small>Our service is still in beta. To save disk space costs (and prevent DOS) our service will delete your GIFs after 15 minutes.</small>
          </h4>
        </hgroup>
        <form id="upload-form" method="post" enctype="multipart/form-data">
          <input name="csrf" type="hidden" value="<?= e($_SESSION['csrf']) ?>">
          <label for="title">Title</label>
          <input name="title" required>
          <label for="description">Description</label>
          <textarea name="description" placeholder="Use <b>, <i>, <u>, <s>, <br> to give your GIF a stylish description!"></textarea>
          <input id="file-input" name="file" type="file" accept=".gif" required>
          <input type="submit" value="Upload">
          <progress id="upload-progress" class="hidden"></progress>
        </form>
      </section>
      <script src="/static/upload.js"></script>
    <?php else : ?>
      <hgroup>
        <h1>YummyGIFs</h1>
        <h2>Host short videos of food 🍕🍔🍦</h2>
      </hgroup>
      <section>
        <div class="centered">
          <a class="centered" href="/register.php" role="button">Register now!</a>
        </div>
      </section>
      <div class="image-gallery">
        <div><img src="/static/pizza.gif" title="cheesy"></div>
        <div><img src="/static/burger.gif" title="not McDonald's burger"></div>
        <div><img src="/static/icecream.gif" title="cool dog"></div>
      </div>
    <?php endif ?>
  </main>
  <?php include('include/footer.php') ?>
</body>

</html>