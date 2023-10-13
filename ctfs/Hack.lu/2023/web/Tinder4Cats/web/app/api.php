<?php

header("Content-Type: application/javascript;");
include 'config.php';

if (!isset($_SESSION['user'])){
    die();
}

// for pagination
$limit = isset($_GET['limit']) ? $_GET['limit'] : 10;
$offset = isset($_GET['offset']) ? $_GET['offset'] : 0;

$favorites = db::get_favorites($_SESSION['user']['id'], $limit, $offset);


function js_filter($str) {
    return str_replace("/", "\\/", addslashes($str));
}


?>

favorites = {
    cats : [
<?php
    foreach ($favorites as $favorite) {
        echo '        "' . js_filter($favorite['cat']) . '",' . PHP_EOL;
    }
    
?>
    ],
    limit : "<?php echo js_filter($limit); ?>",
    offset : "<?php echo js_filter($offset); ?>",
    total : "<?php echo js_filter(count($favorites)); ?>",
};








