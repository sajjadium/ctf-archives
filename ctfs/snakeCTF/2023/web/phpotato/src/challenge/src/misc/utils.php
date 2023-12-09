<?php
$init_app = fn() => (!isset($_SESSION)) ? session_start() : true;

$init_user_hooks = fn() => (!isset($_SESSION['hooks'])) ? $_SESSION['hooks'] = [] : true;

$check_auth = fn() => (!isset($_SESSION['username'])) ? header('Location: /login') || exit('Please authenticate first.') : true;

$check_not_auth = fn() => (isset($_SESSION['username'])) ? header('Location: /home') || exit('You are already logged in.') : true;

$check_admin = fn() => (isset($_SESSION['admin']) && $_SESSION['admin']) ? true : header('Location: /home') || http_response_code(403) && exit('Reserved for admins.');

$check_request_method = fn() => (!isset($_POST['_METHOD'])) ? header('Refresh:0') || http_response_code(400) && exit('Please try again.') : true;

$message = "";
$display_popup = fn($text, &$message) => $message = $text;

$precision = 0;
$set_default_precision = fn(&$precision) =>
    (isset($_GET['precision']) ?
    ($precision = $_GET['precision'])
    : ($precision = DEFAULT_PRECISION)
);

$router_global_methods = [
    'init_app',
    'init_user_hooks',
    'check_auth',
    'check_not_auth',
    'check_admin',
    'check_request_method',
    'set_default_precision',
];
$router_global_vars = [
    'message',
    'precision',
];

// Register global variables for the router
if (isset($register_global)) {
    foreach ($router_global_methods as $method) {
        $register_global($method);
    }

    foreach ($router_global_vars as $var) {
        $register_global($var);
    }

}

// Register possible user hooks
register_new_user_hook('registration_success', $display_popup,
    ["We've sent you a mail pidgeon to confirm your identity.. You can login in the meanwhile.", &$message]);
register_new_user_hook('registration_failure', $display_popup,
    ["You're so unlucky today, try again.", &$message]);
register_new_user_hook('login_success', $display_popup,
    ["Welcome back.", &$message]);
register_new_user_hook('login_failure', $display_popup,
    ["Do I know you?", &$message]);
register_new_user_hook('greet_admin', $display_popup,
    ["Oh Welcome back admin! Have you already checked out <a href='/admin'>/admin</a>?", &$message]);
register_new_user_hook('something_wrong', $display_popup,
    ["Something went wrong, please try again later.", &$message]);
register_new_user_hook('number_added', $display_popup,
    ["Have fun with your number.", &$message]);
register_new_user_hook('pipeline_added', $display_popup,
    ["Your pipeline will be executed ASAP.", &$message]);
register_new_user_hook('pipeline_success', $display_popup,
    ["Your pipeline has finished with success.", &$message]);
register_new_user_hook('pipeline_failure', $display_popup,
    ["Your pipeline has gone mad.", &$message]);
