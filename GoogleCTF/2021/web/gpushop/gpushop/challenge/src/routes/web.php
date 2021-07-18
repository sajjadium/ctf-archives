<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ProductController;
use App\Http\Controllers\CartController;
use App\Http\Controllers\OrderController;

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

Route::get('/products', [ProductController::class, 'index']);
Route::get('/orders', [OrderController::class, 'index']);
Route::get('/order/{order}', [OrderController::class, 'show']);
Route::get('/cart', [CartController::class, 'index']);
Route::post('/cart/clear', [CartController::class, 'clear']);
Route::post('/cart/checkout', [CartController::class, 'checkout']);
Route::post('/cart/{id}', [CartController::class, 'add']);
