<?php

use Illuminate\Support\Facades\Route;
use App\Models\Cocktail;
use App\Http\Controllers\CocktailController;

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

Route::get('/', function (\Illuminate\Http\Request $request) {
    return view('cocktail.welcome');
});

Route::get('/cocktails', 'App\Http\Controllers\CocktailController@index');

Route::get('/cocktail/create', 'App\Http\Controllers\CocktailController@create');
Route::post('/cocktail/create', 'App\Http\Controllers\CocktailController@store');

Route::get('/cocktail/{cocktail}/show', 'App\Http\Controllers\CocktailController@show');

Route::delete('/cocktail/{cocktail}', 'App\Http\Controllers\CocktailController@delete');

Route::get('/cocktail/{cocktail}/edit', 'App\Http\Controllers\CocktailController@edit');
Route::post('/cocktail/{cocktail}/edit', 'App\Http\Controllers\CocktailController@update');

/*
For Example:
TzoxOToiQXBwXE1vZGVsc1xDb2NrdGFpbCI6MzA6e3M6MTM6IgAqAGNvbm5lY3Rpb24iO3M6Njoic3FsaXRlIjtzOjg6IgAqAHRhYmxlIjtzOjk6ImNvY2t0YWlscyI7czoxMzoiACoAcHJpbWFyeUtleSI7czoyOiJpZCI7czoxMDoiACoAa2V5VHlwZSI7czozOiJpbnQiO3M6MTI6ImluY3JlbWVudGluZyI7YjoxO3M6NzoiACoAd2l0aCI7YTowOnt9czoxMjoiACoAd2l0aENvdW50IjthOjA6e31zOjE5OiJwcmV2ZW50c0xhenlMb2FkaW5nIjtiOjA7czoxMDoiACoAcGVyUGFnZSI7aToxNTtzOjY6ImV4aXN0cyI7YjoxO3M6MTg6Indhc1JlY2VudGx5Q3JlYXRlZCI7YjowO3M6Mjg6IgAqAGVzY2FwZVdoZW5DYXN0aW5nVG9TdHJpbmciO2I6MDtzOjEzOiIAKgBhdHRyaWJ1dGVzIjthOjU6e3M6MjoiaWQiO2k6MTtzOjQ6Im5hbWUiO3M6NzoiTmVncm9uaSI7czo2OiJyZWNpcGUiO3M6NTE6IjMwbWwgQ2FtcGFyaSwgMzBtbCBHaW4sIDMwbWwgVmVybW91dGgsIE9yYW5nZSBTbGljZSI7czoxMDoiY3JlYXRlZF9hdCI7TjtzOjEwOiJ1cGRhdGVkX2F0IjtzOjE5OiIyMDIyLTExLTExIDA5OjUyOjU5Ijt9czoxMToiACoAb3JpZ2luYWwiO2E6NTp7czoyOiJpZCI7aToxO3M6NDoibmFtZSI7czo3OiJOZWdyb25pIjtzOjY6InJlY2lwZSI7czo1MToiMzBtbCBDYW1wYXJpLCAzMG1sIEdpbiwgMzBtbCBWZXJtb3V0aCwgT3JhbmdlIFNsaWNlIjtzOjEwOiJjcmVhdGVkX2F0IjtOO3M6MTA6InVwZGF0ZWRfYXQiO3M6MTk6IjIwMjItMTEtMTEgMDk6NTI6NTkiO31zOjEwOiIAKgBjaGFuZ2VzIjthOjA6e31zOjg6IgAqAGNhc3RzIjthOjA6e31zOjE3OiIAKgBjbGFzc0Nhc3RDYWNoZSI7YTowOnt9czoyMToiACoAYXR0cmlidXRlQ2FzdENhY2hlIjthOjA6e31zOjg6IgAqAGRhdGVzIjthOjA6e31zOjEzOiIAKgBkYXRlRm9ybWF0IjtOO3M6MTA6IgAqAGFwcGVuZHMiO2E6MDp7fXM6MTk6IgAqAGRpc3BhdGNoZXNFdmVudHMiO2E6MDp7fXM6MTQ6IgAqAG9ic2VydmFibGVzIjthOjA6e31zOjEyOiIAKgByZWxhdGlvbnMiO2E6MDp7fXM6MTA6IgAqAHRvdWNoZXMiO2E6MDp7fXM6MTA6InRpbWVzdGFtcHMiO2I6MTtzOjk6IgAqAGhpZGRlbiI7YTowOnt9czoxMDoiACoAdmlzaWJsZSI7YTowOnt9czoxMToiACoAZmlsbGFibGUiO2E6Mjp7aTowO3M6NDoibmFtZSI7aToxO3M6NjoicmVjaXBlIjt9czoxMDoiACoAZ3VhcmRlZCI7YToxOntpOjA7czoxOiIqIjt9fQ==

Don't forget to remove this when we'll ship it
*/
Route::get('/test', 'App\Http\Controllers\CocktailController@test');
