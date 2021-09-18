<?php

$arghes = $_GET['args'];
for ( $i=0; $i<count($arghes); $i++ ){
    if ( !preg_match('/^\w+$/', $arghes[$i]) )
        exit();
}
exec("echo " . implode(" ", $arghes));

?>