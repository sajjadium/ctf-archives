@extends('layout')

@section('content')
    <div class="container">
        <div class="row">
            <div class="col-12 text-center pt-5">
            <h1 class="display-one m-5">Cocktail Preview</h1>
                <a href="/cocktails" class="btn btn-outline-primary btn-sm">Go back</a>
                <h1 class="display-one">{{ ucfirst($cocktail->name) }}</h1>
                <p>{{ $cocktail->recipe }}</p> 
                <hr>
            </div>
        </div>
    </div>
@endsection