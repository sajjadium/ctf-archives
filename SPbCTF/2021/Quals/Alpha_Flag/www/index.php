<?php
ob_start();
session_start();
require_once "include/everything.php";

$router = new Misc_Router($_SERVER['REQUEST_URI']);
$page = $router->getPage();
$parameters = $router->getParameters();

$controllerClass = "Controller_404";
if ($page == "") {
    $controllerClass = "Controller_Main";
} elseif ($page == "captcha") {
    $controllerClass = "Controller_Captcha";
} elseif ($page == "compose") {
    $controllerClass = "Controller_Compose";
} elseif ($page == "inbox") {
    $controllerClass = "Controller_Inbox";
} elseif ($page == "login") {
    $controllerClass = "Controller_Login";
} elseif ($page == "logout") {
    $controllerClass = "Controller_Logout";
} elseif ($page == "profile") {
    $controllerClass = "Controller_Profile";
} elseif ($page == "prove") {
    $controllerClass = "Controller_Prove";
} elseif ($page == "register") {
    $controllerClass = "Controller_Register";
}

list ($title, $head, $body) = (new $controllerClass())->Process($parameters);

$template = new Template_Page();
$template->AssignVariable('title', htmlspecialchars($title));
$template->AssignVariable('head', $head);
$template->AssignVariable('body', $body);
$template->AssignVariable('menu', new Template_Menu($page));
echo $template;
