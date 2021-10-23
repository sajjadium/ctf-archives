<?php
$a = $_GET["a"];
$b = $_GET["a"];

if($a == 1 && $b == 0 ){
	echo "0";
} else if($a == 0 && $b == 1){
	echo "1";
} else if($a == 1 && $b == 0){
	echo "1";
} else if($a == 1 && $b == 1){
	echo "2";
} else if($a == 0 && $b == 0){
	echo "0";
} else {
	echo "too hard";
}
echo "\n";