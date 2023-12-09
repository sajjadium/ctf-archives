<?php
require_once 'misc/hooks.php';
require_once 'router.php';

require_once 'misc/config.php';
require_once 'misc/utils.php';
require_once 'misc/pipeline.php';

// General init
register_init_hook($init_app);
register_init_hook($init_user_hooks);
register_init_hook($set_default_precision, [&$precision, $_GET]);
execute_init_hooks();
$init_router();

# Uhh so is this what you want?
register_new_user_hook(
    'show_flag',
    $display_popup,
    ["Uhh all right, here's your flag: " . FLAG, &$message]
);

// Execute user hooks that can be activated
execute_user_hooks();

// Router
$add_route('register', 'GET', 'pages/register.php');
$add_route('register', 'POST', 'pages/users.php');
$add_route('login', 'GET', 'pages/login.php');
$add_route('login', 'POST', 'pages/users.php');
$add_route('home', 'GET', 'pages/home.php');
$add_route('home', 'POST', 'pages/home.php');
$add_route('admin', 'GET', 'pages/admin.php');
$add_route('admin', 'POST', 'pages/numbers.php');
$add_404('pages/404.php');

$route();
