<?php
include_once "../header.php";

$pageName = $_GET["page"];

if (!preg_match('/\w{5,10}\.\w{3,5}/', $pageName)) {
    echo "<p>Invalid page name ):</p>";
    exit();
}

$pageString = file_get_contents("./$pageName");
$sanitized = str_replace("\\", "", $pageString);
$pageObject = json_decode($sanitized, flags: JSON_INVALID_UTF8_IGNORE);

if ($pageObject == null) {
    echo "<p>This page does not exist ):</p>";
    exit();
}

function interpret($section) {
    $content = null;

    switch ($section->type) {
        case "text":
            $content = $section->value;
            break;
        case "link":
            $content = file_get_contents($section->value);
            break;
    }

    return "<$section->tag>$content</$section->tag>";
}

echo "<div class='container my-8 text-center'/>";

foreach ($pageObject->sections as $section) {
    echo interpret($section);
}

echo "</div>";
