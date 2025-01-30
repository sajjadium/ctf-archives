<?php
include_once "header.php";
?>

<h1 class="text-center my-5">Administration</h1>

<h2>Add a magician</h2>
<form enctype="multipart/form-data" method="POST">
    <label for="inputName" class="form-label mt-3">Name</label>
    <input id="inputName" name="name" type="text" required class="form-control"/>
    <label for="inputMagician" class="form-label mt-3">Magician Image</label>
    <input id="inputMagician" name="magician" required type="file" accept="image/jpeg" class="form-control"/>
    <input type="submit" value="Add magician" class="form-control mt-3"/>
</form>

<?php
if ($_SERVER["REQUEST_METHOD"] != "POST") exit();

if (!isset($_FILES["magician"])) {
    echo "<p>You must provide a magician image to upload magicians.</p>";
    exit();
}

if (!isset($_POST["name"])) {
    echo "<p>You must provide a name for your magician.</p>";
    exit();
}

$uploadFile = "./magicians/" . $_POST["name"] . ".magic";
$tmpFile = $_FILES["magician"]["tmp_name"];

$mime = shell_exec("file -b $tmpFile");

if (!preg_match('/\w{1,5} image.*/', $mime)) {
    echo "<p>Invalid upload!</p>";
    exit();
}

if (str_contains($uploadFile, "php")) {
    echo "<p>Invalid magician name!</p>";
    exit();
}

echo "<p>";
if (move_uploaded_file($tmpFile, $uploadFile)) {
    echo "Magician successfully uploaded!";
} else {
    echo "Magician upload failed :(";
}
echo "</p>";
?>

