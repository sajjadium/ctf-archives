<?php
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $str1 = $_POST['string1'] ?? '';
        $str2 = $_POST['string2'] ?? '';

        $hash1 = md5($str1);
        $hash2 = md5($str2);

        if ($str1 == $str2 || strlen($str1) > 100 || strlen($str2) > 100 ||
            strlen($str1) < 5 || strlen($str2) < 5) {
            echo "No\n";
            exit;
        } else if ($hash1 == $hash2) {
            echo file_get_contents("flag.txt");
            exit;
        }
    }
?>

<!DOCTYPE html>
<html>
    <head>
        <title>What?</title>
    </head>
    <body>
        <form method="POST">
            <label for="string1">String 1:</label>
            <input type="text" name="string1" id="string1" required><br />

            <label for="string2">String 2:</label>
            <input type="text" name="string2" id="string2" required><br />

            <input type="submit" value="Compare hashes" />
        </form>
    </body>
</html>
