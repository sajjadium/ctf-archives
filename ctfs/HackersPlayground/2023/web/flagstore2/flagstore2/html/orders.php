<?php
    session_start();
    if(!isset($_SESSION["username"]))
    {
        header('HTTP/1.0 403 Forbidden');
        die("<script>alert('Login, please.'); window.location.href = '/index.php';</script>");
    }

    if($_POST != null)
    {
        echo "Order is submitted! <br />";
        if(!isset($_SESSION["orders"]))
            $_SESSION["orders"] = array();
        array_push($_SESSION["orders"], $_POST);
    }

    if(isset($_SESSION["orders"]) && is_array($_SESSION["orders"]))
    {
        echo "<h3>Order: ". count($_SESSION["orders"]) ."</h3>";
        foreach ($_SESSION["orders"] as $order)
        {
            echo "========================================  <br />";
            echo "No: " . $order["idx"] . "<br />";
            echo "Name: " . $order["name"] . "<br />";
            echo "Price: " . $order["price"] . "<br />";
            echo "========================================  <br />";
        }
    }
?>
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Flag Store v2</title>