@extends('layout')

@section('content')
    <div class="container">
        <div class="row">
            <div class="col-12 text-center pt-5">
            <h1 class="display-one m-5">Cocktail Detail</h1>
                <a href="/cocktails" class="btn btn-outline-primary btn-sm">Go back</a>
                <h1 class="display-one">{{ ucfirst($cocktail->name) }}</h1>
                <p>{{ $cocktail->recipe }}</p> 
                <hr>
                <a href="/cocktail/{{ $cocktail->id }}/edit" class="btn btn-outline-primary">Edit Recipe</a>
                <br><br>
                <form id="delete-frm" class="" action="/cocktail/{{ $cocktail->id }}" method="POST">
                    @method('DELETE')
                    @csrf
                    <button class="btn btn-danger">Delete cocktail</button>
                </form>
            </div>
        </div>
    </div>
@endsection