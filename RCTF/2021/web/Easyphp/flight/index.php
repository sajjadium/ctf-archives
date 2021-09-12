<?php
session_start();
require 'flight/autoload.php';
use flight\Engine;
$app = new Engine();

$username = "admin";
$password = "admin";// you will never know the password

function isdanger($v){
    if(is_array($v)){
        foreach($v as $k=>$value){
            if(isdanger($k)||isdanger($value)){
                return true;
            }
        }
    }else{
        if(strpos($v,"../")!==false){
            return true;
        }
    }
    return false;
}

$app->before("start",function(){
    foreach([$_GET,$_POST,$_COOKIE,$_FILES] as $value){
        if(isdanger($value)){
            die("go away hack");
        }
    }
});
$app->route('/*', function(){
    global $app;
    $request = $app->request();
    $app->render("head",[],"head_content");
    if(stristr($request->url,"login")!==FALSE){
        return true;
    }else{
        if($_SESSION["user"]){
            return true;
        }
        $app->redirect("/login");
    }
    
});


$app->route('/admin', function(){
    global $app;
    $request = $app->request();
    $app->render("admin",["data"=>"./".$request->query->data],"body_content");
    $app->render("template",[]);
});

$app->route("GET /login",function(){
    global $app;
    $request = $app->request();
    $app->render("login",["fail"=>$request->query->fail],"body_content");
    $app->render("template",[]);
});

$app->route("POST /login",function(){
    global $username,$password,$app;
    $request  = $app->request();
    if($request->data->username === $username && $request->data->password === $password){
        $_SESSION["user"] = $username;
        $app->redirect("/");
        return;
    }
    $app->redirect("/login?fail=1");
});

$app->route("GET /",function(){
    global $app;
    $app->render("index",[],"body_content");
    $app->render("template",[]);
});

$app->start();
