<?php

require('JudgeClient.php');

$token = 'YOUR_TOKEN_HERE';

$cSrc = <<<'CODE'
#include <stdio.h>
int main(){
    int a, b;
    scanf("%d%d", &a, &b);
    printf("%d\n", a+b);
    return 0;
}
CODE;

$cSpjSrc = <<<'CODE'
#include <stdio.h>
int main(){
    return 1;
}
CODE;

$cppSrc = <<<'CODE'
#include <iostream>

using namespace std;

int main()
{
    int a,b;
    cin >> a >> b;
    cout << a+b << endl;
    return 0;
}
CODE;

$javaSrc = <<<'CODE'
import java.util.Scanner;
public class Main{
    public static void main(String[] args){
        Scanner in=new Scanner(System.in);
        int a=in.nextInt();
        int b=in.nextInt();
        System.out.println(a + b);
    }
}
CODE;

$py2src = <<<'CODE'
s = raw_input()
s1 = s.split(" ")
print int(s1[0]) + int(s1[1])
CODE;

$py3src = <<<'CODE'
s = input()
s1 = s.split(" ")
print(int(s1[0]) + int(s1[1]))
CODE;


$judgeClient = new JudgeClient($token, 'http://127.0.0.1:12358');

echo "ping:\n";
print_r($judgeClient->ping());

echo "\n\ncompile_spj:\n";
print_r($judgeClient->compileSpj($cSpjSrc, '2', JudgeClient::getLanguageConfigByKey('c_lang_spj_compile')));

echo "\n\nc_judge:\n";
print_r($judgeClient->judge($cSrc, 'c', 'normal', [
    'output' => true
]));

echo "\n\nc_spj_judge:\n";
print_r($judgeClient->judge($cSrc, 'c', 'spj', [
    'spj_version' => '3',
    'spj_config' => JudgeClient::getLanguageConfigByKey('c_lang_spj_config'),
    'spj_compile_config' => JudgeClient::getLanguageConfigByKey('c_lang_spj_compile'),
    'spj_src' => $cSpjSrc,
]));

echo "\n\ncpp_judge:\n";
print_r($judgeClient->judge($cppSrc, 'cpp', 'normal'));

echo "\n\njava_judge:\n";
print_r($judgeClient->judge($javaSrc, 'java', 'normal'));

echo "\n\npy2_judge:\n";
print_r($judgeClient->judge($py2src, 'py2', 'normal'));

echo "\n\npy3_judge:\n";
print_r($judgeClient->judge($py3src, 'py3', 'normal'));