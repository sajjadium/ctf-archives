<?php if(!defined('__MAIN__')) header('Location: /'); ?>
<?php if(!checkLogin()) header('Location: /'); ?>


<?php 
  if( isset($_GET['no'])  ){
    $no = intval($_GET['no']);
    $id = $_SESSION['id'];

    $res = getPost($no);

    if ($id !== $res['val']['writer']) {
      if ($id !== 'admin') {
        die('No');
      } 
    }
    report($no);
  }
?>


<?php require_once WEBROOT . '/components/header.php'; ?>
<?php require_once WEBROOT . '/components/navbar.php'; ?>

<section>
    <div class="py-3">
        <div class="container">       
          <script> alert('Report Complete'); location.href='/'; </script>
        </div>
    </div>
</section>
<?php require_once WEBROOT . '/components/footer.php'; ?>
