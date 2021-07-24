<?php

function filter($var, $case = 0): bool{
    $banned = ["\$_", "eval", "include", "require", "?", ":", "^", "+", "-", "%", "*"];

    foreach($banned as $ban){
        if(strstr($var, $ban)) return True;
    }

    if($case){
        $additional = ["php","/"];
        foreach($additional as $ban){
            if(strstr($var, $ban)) return True;
        }
    }

    return False;
}

function checkLetterNums($var): bool{
    $alphanum = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $cnt = 0;
    for($i = 0; $i < strlen($alphanum); $i++){
        for($j = 0; $j < strlen($var); $j++){
            if($var[$j] == $alphanum[$i]){
                $cnt += 1;
                if($cnt > 4) return True;
            }
        }
    }
    return False;
}