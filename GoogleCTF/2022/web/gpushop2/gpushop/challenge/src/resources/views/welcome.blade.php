<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
         @include('head')
    </head>
    <body>
        @include('nav')

        <main class="container">
          <div class="bg-light p-5 rounded">
            <h1>Welcome!</h1>
            <p class="lead">Are you looking to upgrade your pc? We have the best scalping prices!</p>
          </div>
        </main>
        
</html>
