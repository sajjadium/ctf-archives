<?php

use Illuminate\Support\Facades\Route;
use Illuminate\Http\Request;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});

Route::get('/run', function (Request $request) {
    $cmds = ['ls -al /', 'df -h', 'ss -l', 'ip a', 'ip r', 'ps aux'];
    $cmd = $request->input('cmd');

    if (!is_numeric($cmd) || $cmd < 0 || $cmd > array_key_last($cmds)) {
        throw new Exception('Command not allowed');
        //return view('output', ['stdout' => 'Command not allowed']);
    }
    
    $stdout = shell_exec($cmds[$cmd]);
    return view('output', ['stdout' => $stdout]);
});
