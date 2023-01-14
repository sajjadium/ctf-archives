<?php if (isset($_GET['source'])) highlight_file(__FILE__) && die() ?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="assets/style.css">
    <title>The idek Times</title>
</head>
<body>

<main>
    <nav>
        <h1>The idek Times</h1>
    </nav>

    <?php

        error_reporting(0);
        set_include_path('articles/');

        if (isset($_GET['p'])) {
            $article_content = file_get_contents($_GET['p'], 1);

            if (strpos($article_content, 'PREMIUM') === 0) {
                die('Thank you for your interest in The idek Times, but this article is only for premium users!'); // TODO: implement subscriptions
            }
            else if (strpos($article_content, 'FREE') === 0) {
                echo "<article>$article_content</article>";
                die();
            }
            else {
                die('nothing here');
            }
        }
           
    ?>

    <a href="/?p=flag">
        <article>
            <h2>All about flags</h2>
            <p>Click to view</p>
        </article>
    </a>
    
    <a href="/?p=hello-world">
        <article>
            <h2>My first post!</h2>
            <p>Click to view</p>
        </article>
    </a>

    <a href="/?source" id="source">Source</a>
    
</main>

    
</body>
</html>
