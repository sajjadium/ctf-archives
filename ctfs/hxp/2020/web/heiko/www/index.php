<?php
$manpage = NULL;
$error = NULL;

mb_regex_encoding('utf-8') or die('Invalid encoding');
mb_internal_encoding('utf-8') or die('Invalid encoding');
setlocale(LC_CTYPE, 'en_US.utf8');

if (isset($_GET['page']) && is_string($_GET['page']) && mb_strlen($_GET['page']) > 0) {
    putenv('MANROFFOPT=-P -r'); // Disable the ugly line that groff normally produces
    putenv('PATH=/usr/bin:/bin'); // `man` want this, and I spent way too long to figure that out.

    $arg = $_GET['page'];

    // Make sure there are no options (starting with - or -- or other non-word characters) within
    // the command, but still allow these characters in the middle because otherwise something really
    // simple like 'man fc-cache' or 'man ftw.h' breaks.
    // Also, don't allow shenanigans with ' or " that might allow someone to smuggle a few -- in there.
    if (mb_ereg('(^|\\s+)\W+', $arg) || mb_strpos($arg, '"', 0, 'utf-8') || mb_strpos($arg, '\'', 0, 'utf-8')) {
        $arg = mb_ereg_replace('(^|\\s+)\W+', '\\1', $arg);
        $arg = mb_ereg_replace('["\']', '', $arg);
        $words = mb_split(' ', $arg);
        $last_word = $words ? end($words) : '';
        if (mb_strlen($last_word) > 0) {
            $urlsafe = urlencode($last_word);
            $htmlsafe = htmlentities($last_word, ENT_QUOTES | ENT_SUBSTITUTE | ENT_HTML5, 'utf-8');
            $fix = ' Did you mean <a href="/?page=' . $urlsafe . '">' . $htmlsafe . '</a> instead?';
        } else {
            $fix = '';
        }
        $error = 'Your query contains invalid characters.' . $fix;
    }

    if (mb_strlen($arg) > 0) {
        $arg = escapeshellcmd($arg); // Pass spaces through. Otherwise, we can't 'man git diff'
        $manpage = shell_exec('/usr/bin/man --troff-device=html --encoding=UTF-8 ' . $arg);
        if ($manpage !== NULL) {
            // Do some sensible styling. Sorry about the regex hell.
            // (And yes, I know what happens when you try to parse HTML with regex...)
            $start = mb_strripos($manpage, '<body>', 0, 'utf-8');
            $stop = mb_stripos($manpage, '</body>', 0, 'utf-8');
            $manpage = ($start <= $stop) ? mb_substr($manpage, $start, $stop - $start, 'utf-8') : '';
            // Unfortunately, HTML is case-insensitive, so use eregi here.
            $manpage = mb_eregi_replace('(</h[2-6]>)', '\\1<a class="top" href="#">↑</a>', $manpage);
            $manpage = mb_eregi_replace(
                '<b>([a-zA-Z0-9-_]+)</b>\\(([0-9a-z][a-z]?)\\)',
                '<a class="rel" href="/?page=\\1.\\2"><b>\\1</b>(\\2)</a>',
                $manpage
            );
            $manpage = mb_eregi_replace(
                '([a-zA-Z0-9-_]+)</b>\\(([0-9a-z][a-z]?)\\)',
                '</b><a class="rel" href="/?page=\\1.\\2"><b>\\1</b>(\\2)</a>',
                $manpage
            );
            $manpage = mb_eregi_replace(
                '([a-zA-Z0-9-_]+)\\(([0-9a-z][a-z]?)\\)',
                '<a class="rel" href="/?page=\\1.\\2"><b>\\1</b>(\\2)</a>',
                $manpage
            );
        } else {
            $error = 'Could not find a manpage about ' . $arg;
        }
    }
}
?>
<!DOCTYPE html>
<html>
    <head>
        <title>MaaS</title>
        <meta charset="utf-8" />
        <style>
            * { font-family: monospace; margin: 1ch 0; padding: 0; text-decoration: none; }
            html { margin: auto; max-width: 80ch; padding: 2ch; font-size: 1.25em; }
            header { margin: 2ch 0 4ch 0; }
            header h1, header h2, header h3, header h4 { text-align: center; margin: 0; }
            input[type="text"] { width: 100%; }
            .error { color: #f00; }
            .error a { color: #800; }
            .manpage h1, .manpage h2, .manpage h3, .manpage h4, .manpage h5 { display: inline-block; }
            .manpage a:not(:first-of-type):not(:last-of-type) { margin: -2ch 0; display: block; }
            .manpage a:first-of-type { margin-bottom: -2ch; display: block; }
            .manpage a:last-of-type { margin-top: -2ch; display: block; }
            .manpage a.top { display: inline !important; margin: 0 0 0 1ch !important; font-size: 1em; }
            .manpage a.rel { display: inline !important; }
            .manpage p a[href]:not(.top):not(.rel) { display: inline; pointer-events: none; cursor: default; color: #000; }
            .manpage p a[href]:not(.top):not(.rel)::after { content: " [" attr(href) "]"; font-size: 0.75em; }
        </style>
    </head>
    <body>
        <header>
            <h1>MaaS</h1>
            <h4>Manpage-as-a-Service</h4>
        </header>

        <p>Welcome to <strong>Manpage-as-a-Service</strong>, the [marketing bullsh*t here]</p>
        <form action="/" method="GET">
            <input type="text" name="page" placeholder="What do you want to know about?" />
        </form>
        <?php if ($error !== NULL) { ?>
        <div class="error">
            <?= $error ?>
        </div>
        <?php } ?>
        <div class="manpage">
        <?= $manpage ?: '' ?>
        </div>
    </body>
</html>
