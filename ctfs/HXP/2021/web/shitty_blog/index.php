<?php
// TODO: fully implement multi-user / guest feature :(

$secret = 'SECRET_PLACEHOLDER';
$salt = '$6$'.substr(hash_hmac('md5', $_SERVER['REMOTE_ADDR'], $secret), 16).'$';

if(! isset($_COOKIE['session'])){
    $id = random_int(1, PHP_INT_MAX);
    $mac = substr(crypt(hash_hmac('md5', $id, $secret, true), $salt), 20);
}
else {
    $session = explode('|', $_COOKIE['session']);
    if( ! hash_equals(crypt(hash_hmac('md5', $session[0], $secret, true), $salt), $salt.$session[1])) {
        exit();
    }
    $id = $session[0];
    $mac = $session[1];
}
setcookie('session', $id.'|'.$mac);
$sandbox = './data/'.md5($salt.'|'.$id.'|'.$mac);
if(! is_dir($sandbox)) {
    mkdir($sandbox);
}

$db = new PDO('sqlite:'.realpath($sandbox).'/blog.sqlite3');
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);

$schema = "
    CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, name VARCHAR(255));
    CREATE TABLE IF NOT EXISTS entry (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, content TEXT);

    INSERT OR IGNORE INTO user (id, name) VALUES (0, 'System');
    INSERT OR IGNORE INTO entry (id, user_id, content) VALUES (0, 0, 'Welcome to your new blog - 🚩🚩🚩 ʕ•́ᴥ•̀ʔっ🤎 🚩🚩🚩');
";
$db->exec($schema);

function get_entries($db){
    $sth = $db->query('SELECT id, user_id, content FROM entry ORDER BY id DESC');
     return $sth->fetchAll(); 
}

function get_user($db, $user_id) : string {
    foreach($db->query("SELECT name FROM user WHERE id = {$user_id}") as $user) {
        return $user['name'];
    }
    return 'me';
}

function insert_entry($db, $content, $user_id) {
    $sth = $db->prepare('INSERT INTO entry (content, user_id) VALUES (?, ?)');
    $sth->execute([$content, $user_id]);
}

function delete_entry($db, $entry_id, $user_id) {
    $db->exec("DELETE from entry WHERE {$user_id} <> 0 AND id = {$entry_id}");
}

if(isset($_POST['content'])) {
    insert_entry($db, htmlspecialchars($_POST['content']), $id);

    header('Location: /');
    exit;
}

$entries = get_entries($db);

if(isset($_POST['delete'])) {
    foreach($entries as $key => $entry) {
        if($_POST['delete'] === $entry['id']){
            delete_entry($db, $entry['id'], $entry['user_id']);
            break;
        }
    }

    header('Location: /');
    exit;
}

foreach($entries as $key => $entry) {
    $entries[$key]['user'] = get_user($db, $entry['user_id']);
}

?>
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>My shitty Blog</title>
    <link rel="icon" type="image/png" href="/favicon.png"/>
  </head>
  <body>
    <h1>My shitty blog</h1>
    <form method="post">
        <textarea cols="50" rows="10" name="content"></textarea>
        <input type="submit" value="Post">
    </form>
    <?php foreach($entries as $entry):?>
        <div>
            <p><?= $entry['content'] ?></p>
            <small>By <?=  $entry['user'] ?> </small>
            <form method="post">
                <input type="hidden" name="delete" value="<?= $entry['id'] ?>">
                <input type="submit" value="Delete">
            </form>
        </div>
        <hr>
    <?php endforeach ?>

  </body>
</html>
