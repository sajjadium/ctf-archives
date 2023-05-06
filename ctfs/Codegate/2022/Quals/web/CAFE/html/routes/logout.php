<?php if(!defined('__MAIN__')) header('Location: /'); ?>
<?php if(!checkLogin()) header('Location: /'); ?>
<?php session_destroy(); ?>

<?php header('Location: /'); ?>