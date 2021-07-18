<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
         @include('head')
    </head>
    <body>
        @include('nav')

        <main class="container">
            @if ($orders->isEmpty())
            <div class="alert alert-warning" role="alert">
                Buy something!
            </div>
            @endif            
            <ul class="list-group">
            @foreach ($orders as $o)
              <li class="list-group-item"><a href="/order/{{ $o->id }}">{{ $o->id }}</a></li>
            @endforeach
            </ul>
        </main>
        
</html>
