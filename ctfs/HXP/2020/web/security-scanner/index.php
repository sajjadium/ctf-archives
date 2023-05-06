<?php

session_start();
if (!isset($_SESSION['sandbox'])) {
    $id = '';
    while(strlen($id) < 10) {
        $b = random_bytes(1);
        if(ord($b) > 32 && ord($b) != 0x7f) {
            $id .= $b;
        }
    }
    $_SESSION['sandbox'] = $id;
}

echo '<h1>Sandbox</h1>';
echo '<code>'.base64_encode($_SESSION['sandbox']).'</code>';  

$m = new Memcached();
$m->addServer('127.0.0.1', 11211);

$url = strval($_GET['url']);
if ($m->get($_SESSION['sandbox'].$url) !== 'OK') {
    if(preg_match('/^[0-9a-zA-Z:\.\/-]{1,64}$/', $url) !== 1) {
        die('security :(');
    }

    $git_check = "001e# service=git-upload-pack\n";
    $data = file_get_contents($url .'/info/refs?service=git-upload-pack');
    if ($data  === FALSE || substr($data, 0, strlen($git_check)) !== $git_check) {
        die("doesn't look like git :(");
    }

    $m->set($_SESSION['sandbox'].$url, 'OK', time() + 300);
}

$output = [];
$return_var = 1;
exec("timeout -s KILL 3 git ls-remote --tags -- $url", $output, $return_var);
if($return_var !== 0) {
    die('analysis failed :(');
}

echo '<h1>Analysis</h1>';
echo "URL: ${url}";
echo '<h2>Tags</h2>';
echo '<ul>';

foreach($output as $l) {
    echo "<li><code>${l}</code></li>";
}
echo '</ul>';

echo '<h2>Result</h2>';

if(TRUE) { // patented algorithm (tm)
    echo 'Likely insecure :('; 
}
