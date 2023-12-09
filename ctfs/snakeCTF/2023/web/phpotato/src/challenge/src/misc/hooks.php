<?php
$init_hooks = [];
$user_hooks = [];

function register_init_hook(&$fn, $args = [])
{
    global $init_hooks;

    $init_hooks[] = [$fn, $args];
}
function execute_init_hooks()
{
    global $init_hooks;

    foreach ($init_hooks as [$hook, $args]) {
        $hook(...$args);
    }

    $init_hooks = [];
}

function register_user_hook($name, &$callback, $args = [])
{
    global $user_hooks;

    $user_hooks[$name] = [ &$callback, $args];
}

function register_new_user_hook($name, &$callback, $args = [])
{
    global $user_hooks;

    if (!array_key_exists($name, $user_hooks)) {
        register_user_hook($name, $callback, $args);
    }

}

function set_user_hook($name)
{
    $_SESSION['hooks'][] = $name;
}

function execute_user_hooks()
{
    global $user_hooks;

    foreach ($_SESSION['hooks'] as $name) {
        [$callback, $args] = $user_hooks[$name];
        $callback(...$args);
    }
    $_SESSION['hooks'] = [];
}
