<?php if(!defined('__MAIN__')) header('Location: /'); ?>
<?php if(!checkLogin()) header('Location: /'); ?>


<?php 
  if( isset($_GET['no'])  ){
    $no = intval($_GET['no']);
    $id = $_SESSION['id'];

    $res = getPost($no);

    if ($id !== $res['val']['writer']) {
      if ($id !== 'admin') { // admin cat see all posts
        die('No');
      } 
    }
    
    updateViews($no);

  }
?>


<?php require_once WEBROOT . '/components/header.php'; ?>
<?php require_once WEBROOT . '/components/navbar.php'; ?>

<section>
    <div class="py-3">
        <div class="container">       
          <h1><?= $res['val']['title'] ?></h1> <a href="/report?no=<?= $no ?>">report</a>
          <hr>
          <?= $res['val']['content'] ?>
        </div>
    </div>
</section>
<?php require_once WEBROOT . '/components/footer.php'; ?>
