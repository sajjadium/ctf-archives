<?php

if (php_sapi_name() !== 'cli') {
    echo "flag{fake}";
    die();
}

$datadir = sys_get_temp_dir() . '/data';

while (true) {
    sleep(60 * 10);

    echo "Running cleanup\n";
    system("rm -r $datadir/*");
}
