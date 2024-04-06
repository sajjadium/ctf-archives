<?php
if (isset($_GET["username"])) {
    $encodedUsername = str_replace("=", "", $_GET["username"]);

    // Username is not admin
    if ($encodedUsername === "YWRtaW4") {
        $decodedUsername = "";
    } else {
        $decodedUsername = base64_decode($encodedUsername);

        // Check if the username contains only alphanumeric characters and underscores
        if (!preg_match('/^[a-zA-Z0-9_]+$/', $decodedUsername)) {
            $decodedUsername = "";
        }
    }
}

$flagContents = file_get_contents("flag.txt");
$flagMessage = "<pre>" . htmlspecialchars($flagContents) . "</pre>";
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SpaceNotes</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <?php if (!isset($_GET["username"])): ?>
            <h1>SpaceNotes</h1>
            <p>Specify a username in base64 to access your notes.</p>
            <p>Example: <a href="/?username=<?php echo base64_encode("toto"); ?>">toto</a></p>
            <p>🛑 Admin notes are restricted 🛑</p>
        
        <?php else: ?>
            <?php if ($decodedUsername === ""): ?>
                <h1>Error</h1>
                <p class="error">Invalid username</p>

            <?php elseif ($decodedUsername === "admin"): ?>
                <h1>🟢 Welcome admin! 🟢</h1>
                <p><?php echo $flagMessage; ?></p>

            <?php else: ?>
                <h1>🟠 Welcome <?php echo htmlspecialchars($decodedUsername); ?>! 🟠</h1>
                <p>Nothing here 🚀</p>
                
            <?php endif; ?>
        <?php endif; ?>
    </div>
</body>
</html>