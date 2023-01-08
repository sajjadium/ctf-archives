<?php
$password = exec("openssl rand -hex 64");

$stretched_password = "";
for($a = 0; $a < strlen($password); $a++) {
    for($b = 0; $b < 64; $b++)
        $stretched_password .= $password[$a];
}

echo "Fear my 4096 byte password!\n> ";

$h = password_hash($stretched_password, PASSWORD_DEFAULT);

while (FALSE !== ($line = fgets(STDIN))) {
    if(password_verify(trim($line), $h)) die(file_get_contents("flag"));
    echo "> ";
}
die("No!");

?>

