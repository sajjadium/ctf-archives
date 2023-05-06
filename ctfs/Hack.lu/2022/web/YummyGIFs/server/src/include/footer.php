<div id="footer" class="container">
  <?php if ($success) : ?>
    <div class="alert alert-success" role="alert"><?= e($success) ?></div>
  <?php elseif ($error) : ?>
    <div class="alert alert-error" role="alert"><?= e($error) ?></div>
  <?php endif ?>
  </div>
<script src="/static/footer.js"></script>