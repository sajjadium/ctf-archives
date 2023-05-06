<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
        @include('head')
    </head>
    <body>
        @include('nav')

        <main class="container">
            <div>
                <h4 class="mb-3">Order Information</h4>
                <div>#ID {{ $order->id }}</div>
                <div>Total {{ $order->total }} &#x039e;</div>
                <div>Shipping Address: {{ $order->address }}</div>
                <hr class="my-4">
                <h4 class="mb-3">Payment</h4>
                <div>Please send your payment to the following address:</div>
                <div><a href="https://etherscan.io/address/{{$order->wallet}}">{{ $order->wallet }}</a></div>
            </div>
            <br>
            <div>
                @if ($paid)
                <div class="alert alert-primary" role="alert">Payment confirmed.</div>
                @endif
                @if ($flag)
                <div class="alert alert-success" role="alert">The flag is {{ $flag }}</div>
                @endif                
            </div>
        </main>
        
</html>
