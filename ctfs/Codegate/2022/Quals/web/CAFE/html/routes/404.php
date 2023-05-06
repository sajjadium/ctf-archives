<?php if(!defined('__MAIN__')) header('Location: /'); ?>

<?php require_once WEBROOT . '/components/header.php'; ?>
<?php require_once WEBROOT . '/components/navbar.php'; ?>

<section>
    <div class="py-3">
        <div class="container" style="text-align: center; font-size: 72px">       
            <p> <b><?= $_SERVER['REQUEST_URI']; ?></b> is not here. </p>
        </div>
    </div>
</section>

<?php require_once WEBROOT . '/components/footer.php'; ?>