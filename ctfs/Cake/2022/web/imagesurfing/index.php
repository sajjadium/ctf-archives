<?php
const IMAGE_MIME = ['image/jpeg', 'image/png', 'image/gif'];

function get_image($url) {
    /* Open URL */
    $data = @file_get_contents($url);
    if ($data == false)
        return array("Cannot fetch file", false);

    /* Check file size */
    if (strlen($data) > 1024*1024*16)
        return array("File size is too large", false);

    /* Get mime type */
    $tmp = tmpfile();
    fwrite($tmp, $data);
    fflush($tmp);
    $mime = mime_content_type(stream_get_meta_data($tmp)['uri']);
    fclose($tmp);

    /* Check */
    if (in_array($mime, IMAGE_MIME)) {
        return array($mime, $data);
    } else {
        return array("Invalid image file", false);
    }
}

if (!empty($_GET['url'])) {
    list($mime, $img) = get_image($_GET['url']);
    if ($img === false) {
        $err = $mime;
    }
}
?>
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>ImageSurfing</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/purecss@2.1.0/build/pure-min.css" integrity="sha384-yHIFVG6ClnONEA5yB5DJXfW2/KC173DIQrYoZMEtBvGzmf0PKiGyNEqe9N6BNDBH" crossorigin="anonymous">
    </head>
    <body style="text-align: center;">
        <h1>Image Viewer</h1>
        <form class="pure-form" action="/" method="GET">
            <input type="text" placeholder="URL" name="url" style="width: 50%"
                   value="<?= empty($_GET['url'])
                            ? "https://c.tenor.com/NFjEeHbk-zwAAAAC/cat.gif"
                            : htmlspecialchars($_GET['url']) ?>">
            <input class="pure-button pure-button-primary"
                   type="submit" value="View!">
        </form>
        <br>
        <?php if (isset($err)) { ?>
            <p>Error: <?= htmlspecialchars($err) ?></p>
        <?php } ?>
        <?php if (!empty($img)) { ?>
            <img alt="<?php htmlspecialchars($_GET['url']) ?>"
                 style="max-width: 30%;"
                 src="data:<?= $mime ?>;base64,<?= base64_encode($img) ?>">
        <?php } ?>
    </body>
</html>
