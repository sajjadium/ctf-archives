<?php
function h($s) { return htmlspecialchars($s); }
function craft_url($service, $owner, $repo, $branch, $file) {
    if (strpos($service, "github") !== false) {
        /* GitHub URL */
        return $service."/".$owner."/".$repo."/".$branch."/".$file;

    } else if (strpos($service, "gitlab") !== false) {
        /* GitLab URL */
        return $service."/".$owner."/".$repo."/-/raw/".$branch."/".$file;

    } else if (strpos($service, "bitbucket") !== false) {
        /* BitBucket URL */
        return $service."/".$owner."/".$repo."/raw/".$branch."/".$file;

    }

    return null;
}

$service = empty($_GET['service']) ? "" : $_GET['service'];
$owner   = empty($_GET['owner'])   ? "ptr-yudai" : $_GET['owner'];
$repo    = empty($_GET['repo'])    ? "ptrlib"    : $_GET['repo'];
$branch  = empty($_GET['branch'])  ? "master"    : $_GET['branch'];
$file    = empty($_GET['file'])    ? "README.md" : $_GET['file'];

if ($service) {
    $url = craft_url($service, $owner, $repo, $branch, $file);
    if (preg_match("/^http.+\/\/.*(github|gitlab|bitbucket)/m", $url) === 1) {
        $result = file_get_contents($url);
    }
}
?>
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>GitFile Explorer</title>
        <link rel="stylesheet" href="https://cdn.simplecss.org/simple-v1.css">
    </head>
    <body>
        <header>
            <h1>GitFile Explorer API Test</h1>
            <p>Simple API to download files on GitHub/GitLab/BitBucket</p>
        </header>
        <main>
            <form method="GET" action="/">
                <label for="service">Service: </label>
                <select id="service" name="service" autocomplete="off">
                    <option value="https://raw.githubusercontent.com" <?= strpos($service, "github") === false ? "" : 'selected="selected"' ?>>GitHub</option>
                    <option value="https://gitlab.com" <?= strpos($service, "gitlab") === false ? "" : 'selected="selected"' ?>>GitLab</option>
                    <option value="https://bitbucket.org" <?= strpos($service, "bitbucket") === false ? "" : 'selected="selected"' ?>>BitBucket</option>
                </select>
                <br>
                <label for="owner">GitHub ID: </label>
                <input id="owner" name="owner" type="text" placeholder="Repository Owner" value="<?= h($owner); ?>">
                <br>
                <label for="repo">Repository Name: </label>
                <input id="repo" name="repo" type="text" placeholder="Repository Name" value="<?= h($repo); ?>">
                <br>
                <label for="branch">Branch: </label>
                <input id="branch" name="branch" type="text" placeholder="Branch Name" value="<?= h($branch); ?>">
                <br>
                <label for="file">File Path: </label>
                <input id="file" name="file" type="text" placeholder="README.md" value="<?= h($file); ?>">
                <br>
                <input type="submit" value="Download">
            </form>
            <?php if (isset($result)) { ?>
                <br>
                <?php if ($result === false) { ?>
                    <p>Not Found :(</p>
                <?php } else {?>
                    <textarea rows="20" cols="40"><?= h($result); ?></textarea>
                <?php } ?>
            <?php } ?>
        </main>
        <footer>
            <p>zer0pts CTF 2022</p>
        </footer>
    </body>
</html>
