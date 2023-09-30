<?php

if(!isset($_POST['post_id']))
    die("Missing id");

$post_id = $_POST['post_id'];
// check if match the regex
if (!preg_match('/^[a-f0-9]{40}$/', $post_id)) 
    die("Invalid post id");


$CHALLENGE_URL = getenv("URL") ?: "http://leakynote.challs.todo.it:1337/";
$ADMIN_PASSWORD = getenv("ADMIN_PASSWORD") ?: "REDACTED";
$HEADLESS_HOST = getenv("HEADLESS_HOST") ?: "http://headless:5000/";
$HEADLESS_AUTH = getenv("HEADLESS_AUTH") ?: "REDACTED";
$POST_URL = $CHALLENGE_URL."post.php?id=".$post_id;

//The data you want to send via POST
$fields = [
    'browser'      => 'chrome',
    'timeout'  => 60 * 15,
    'actions'  => [
        [
            "type"=> "request",
            "url"=> $CHALLENGE_URL."login.php",
            "method"=> "GET"
        ],
        [
            "type"=> "type",
            "element"=> 'input[name="name"]',
            "value"=> "admin"
            
        ],
        [
            "type"=> "type",
            "element"=> 'input[name="pass"]',
            "value"=> $ADMIN_PASSWORD
        ],
        [
            "type"=> "click",
            "element"=> 'input[type="submit"]'
        ],
        [
            "type"=> "sleep",
            "time"=> 1
        ],
        [
            "type"=> "request",
            "url"=> $POST_URL,
            "method"=> "GET"
        ],
        [
            "type"=> "sleep",
            "time"=> 60*15
        ]
    ]
];

//url-ify the data for the POST
$fields_string = json_encode($fields);

//open connection
$ch = curl_init();

//set the url, number of POST vars, POST data
curl_setopt($ch,CURLOPT_URL, $HEADLESS_HOST);
curl_setopt($ch,CURLOPT_POST, true);
curl_setopt($ch,CURLOPT_POSTFIELDS, $fields_string);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "Content-Type: application/json",
    "X-Auth: $HEADLESS_AUTH"
]);
echo $HEADLESS_AUTH;
//So that curl_exec returns the contents of the cURL; rather than echoing it
curl_setopt($ch,CURLOPT_RETURNTRANSFER, true); 

//execute post
$result = curl_exec($ch);
echo $result;