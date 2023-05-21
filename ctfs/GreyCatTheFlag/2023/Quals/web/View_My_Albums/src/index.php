<?php

include('Albums.php');
include('db_creds.php');

class UserPrefs {
    private $props = array();
    public $font_size;
    public $font_color;
    public $background_color;
    public $language;
    public $timezone;
    
    public function __set($name, $value) {
        $this->props[$name] = $value;
    }
    
    public function __get($name) {
        return $this->props[$name];
    }
    
}

$allowed_langs = array("en", "fr", "de");

if (isset($_COOKIE['prefs'])) {
    $prefs = unserialize($_COOKIE['prefs']);
    if (!($prefs instanceof UserPrefs)) {
        echo "Unrecognized data: ";
        var_dump($prefs);
        exit;
    }
} else {
    $prefs = new UserPrefs();
    $prefs->font_size = "medium";
    $prefs->font_color = "black";
    $prefs->background_color = "white";
    $prefs->language = "en";
    $prefs->timezone = "UTC";
    $prefs->frob_enabled = true;
    $prefs->frob_level = 11;
    setcookie("prefs", serialize($prefs));
}

if (!in_array($prefs->language, $allowed_langs)) {
    $prefs->language = "en";
}

$albums = new Albums(new MysqlRecordStore($mysql_host, $mysql_user, $mysql_password, $mysql_database, 'albums'));

?>
<!DOCTYPE html>
<html>
    <head>
        <title>Cool Album Viewer</title>
        <style>
            body {
                font-family: sans-serif;
                font-size: <?php echo $prefs->font_size; ?>;
                color: <?php echo $prefs->font_color; ?>;
                background-color: <?php echo $prefs->background_color; ?>;
            }
        </style>
    </head>
    <body>
        <h1><?php include("greetings/$prefs->language"); ?></h1>
        <?php
        if (isset($_GET['id'])) {
            $album = $albums->getAlbum((int) $_GET['id']);
            if ($album) {
                ?>
                <h2><?php echo $album->name; ?></h2>
                <p>Artist: <?php echo $album->artist; ?></p>
                <p>Year: <?php echo $album->year; ?></p>
                <p>Genre: <?php echo $album->genre; ?></p>
                <?php
            } else {
                ?>
                <p>Sorry, that album doesn't exist.</p>
                <?php
            }
        }
        ?>
        <h2>Albums</h2>
        <ul>
            <?php foreach ($albums->getAllAlbums() as $album) { ?>
                <li><a href="?id=<?php echo $album->id; ?>"><?php echo $album->name; ?></a></li>
            <?php } ?>
        </ul>
    </body>
</html>