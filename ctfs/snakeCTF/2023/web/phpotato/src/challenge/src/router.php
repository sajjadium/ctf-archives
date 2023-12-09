<?php
$pages = [];
$globals = [];
$req_page = null;
$req_method = null;

$init_router = function () use (&$pages) {
    global $pages;
    global $req_page;
    global $req_method;

    $req_page = $_GET['page'];
    $req_method = $_SERVER['REQUEST_METHOD'];
    $pages = [];
};

$add_route = function ($page_name, $method, $page_file) use (&$pages) {
    global $pages;

    if (!array_key_exists($page_name, $pages)) {
        $pages[$page_name] = [];
    }

    $pages[$page_name][$method] = $page_file;
};

$add_404 = function ($page_file) use (&$pages) {
    global $pages;

    $pages['404'] = $page_file;
};

$register_global = function ($name) {
    global $globals;

    $globals[] = $name;
};

$route = function () use (&$pages) {
    global $globals;
    global $pages;
    global $req_page;
    global $req_method;

    // Include all globals variable which are registered
    foreach ($globals as $var) {
        global $$var;
    }

    // Execute routing function
    try {
        if (array_key_exists($req_page, $pages) && array_key_exists($req_method, $pages[$req_page])) {
            include_once $pages[$req_page][$req_method];
        } else {
            include_once $pages['404'];
        }
        // Render result
        $render();
    } catch (Error $e) {
        http_response_code(500);
        print('Rendering Error occurred!\n' .
            'Please contact the nearest locally available administrator and report him the file' .
            print_r($pages[$req_page][$req_method], true) . '\n');
    }
};
