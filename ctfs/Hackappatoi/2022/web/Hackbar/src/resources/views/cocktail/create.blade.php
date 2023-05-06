@extends('layout')
@section('content')

    <div class="container">
        <div class="row">
            <div class="col-12 pt-2">
                <a href="/cocktails" class="btn btn-outline-primary btn-sm">Go back</a>
                <div class="border rounded mt-5 pl-4 pr-4 pt-4 pb-4">
                    <h1 class="display-4">Create Cocktail Recipe</h1>
                    <hr>
                    <form action="" method="POST">
                        @csrf
                        <div class="row">
                            <div class="control-group col-12">
                                <label for="name">Cocktail Name</label>
                                <input type="text" id="name" class="form-control" name="name"
                                       placeholder="Enter cocktail name" required>
                            </div>
                            <div class="control-group col-12 mt-2">
                                <label for="recipe">Cocktail Recipe</label>
                                <input id="recipe" class="form-control" name="recipe" placeholder="Enter Cocktail Recipe"
                                          rows=""  required></input>
                            </div>
                        </div>
                        <div class="row mt-2">
                            <div class="control-group col-12 text-center">
                                <button id="btn-submit" class="btn btn-primary">
                                    Create
                                </button>
                            </div>
                        </div>
                        
                        @if(session()->get('success') == 'true')
                        <div class="row mt-2">
                                <div class="control-group col-12 text-center alert alert-success" role="alert">
                                    Recipe Added Successfully
                                </div>
                        </div>
                        @endif()
                    </form>
                </div>

            </div>
        </div>
    </div>

@endsection