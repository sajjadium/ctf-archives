k<?php

// Hardcoded list of users and their passwords
$users = [
    'user1' => getenv("PASSWORD1"),
    'user2' => getenv("PASSWORD2"),
    // Add more users as needed
];

// Hardcoded flag
$flag = getenv("FLAG");

// Function to generate a random nonce
function generateNonce()
{
    return md5(mt_rand());
}

// Function to calculate the digest hash
function calculateDigestHash($username, $realm, $password, $method, $uri, $nonce, $cnonce, $qop, $nc)
{
    $A1 = md5("{$username}:{$realm}:{$password}");
    $A2 = md5("{$method}:{$uri}");
    $response = md5("{$A1}:{$nonce}:{$nc}:{$cnonce}:{$qop}:{$A2}");
    return $response;
}

// Function to send the authentication challenge
function sendAuthenticationChallenge()
{
    header('HTTP/1.1 401 Unauthorized');
    header('WWW-Authenticate: Digest realm="Restricted Area",qop="auth",nonce="' . generateNonce() . '",opaque="' . md5('Restricted Area') . '"');
    exit;
}

// Check if the user is already authenticated
if (isset($_SERVER['PHP_AUTH_DIGEST'])) {
    $data = [];
    $needed_parts = ['nonce' => 1, 'nc' => 1, 'cnonce' => 1, 'qop' => 1, 'username' => 1, 'uri' => 1, 'response' => 1];
    $matches = [];
    
    preg_match_all('@(\w+)=(?:(["\'])([^\2]+?)\2|([^\s,]+))@', $_SERVER['PHP_AUTH_DIGEST'], $matches, PREG_SET_ORDER);
    
    foreach ($matches as $m) {
        $data[$m[1]] = $m[3] ? $m[3] : $m[4];
        unset($needed_parts[$m[1]]);
    }
    
    if (empty($needed_parts)) {
        $user = $data['username'];
        $realm = 'Restricted Area';
        $password = $users[$user];
        $method = $_SERVER['REQUEST_METHOD'];
        $uri = $_SERVER['REQUEST_URI'];
        $nonce = $data['nonce'];
        $cnonce = $data['cnonce'];
        $qop = $data['qop'];
        $nc = $data['nc'];
        
        $expected_response = calculateDigestHash($user, $realm, $password, $method, $uri, $nonce, $cnonce, $qop, $nc);
        
        if ($data['response'] === $expected_response) {
            // User is authenticated
            echo "Flag: $flag";
        }
    }
}

// If the user is not authenticated, send the authentication challenge
sendAuthenticationChallenge();

?>

