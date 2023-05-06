<?php
function ms($s){
    return htmlspecialchars($s, ENT_QUOTES);
}

function print_footer(){
    printf("<div class='footer'> %s | STOINKS AG</div><br>" , @date('Y'));
}

function error($error){
    printf("<div class='alert alert-danger'><strong>%s</strong></div>", ms($error));
    print_footer();
    exit();
}

function success($success){
    printf("<div class='alert alert-success'><strong>%s</strong></div>", ms($success));
}

function get_ip(){
    if (!empty($_SERVER['X-Real-IP'])) {
        return $_SERVER['X-Real-IP'];
    } 
    if (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
        return $_SERVER['HTTP_X_FORWARDED_FOR'];
    } 
    else {
        return $_SERVER['REMOTE_ADDR'];
    }
}

function redirect($url, $s=0) {
    echo "<meta http-equiv='refresh' content='$s;$url'>";
}


function gen_secure_url($f){
    $secret = getenv('SECURE_URL_SECRET');
    $hash = md5("{$secret}|{$f}|{$secret}");
    $url = "download.php?h={$hash}&file_name={$f}";
    return $url;
}

function check_url(){
    // fixed bypasses with arrays in get parameters
    $query  = explode('&', $_SERVER['QUERY_STRING']);
    $params = array();
    foreach( $query as $param ){
        // prevent notice on explode() if $param has no '='
        if (strpos($param, '=') === false){
            $param += '=';
        }
        list($name, $value) = explode('=', $param, 2);
        $params[urldecode($name)] = urldecode($value);
    }

    if(!isset($params['file_name']) or !isset($params['h'])){
        return False;
    }

    $secret = getenv('SECURE_URL_SECRET');
    $hash = md5("{$secret}|{$params['file_name']}|{$secret}");

    if($hash === $params['h']){
        return True;
    }
    return False;
    
}

?>