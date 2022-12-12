<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Cocktail;

class CocktailController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        $cocktails = Cocktail::all(); //fetch all cocktails from DB
        return view('cocktail.list', ['cocktails' => $cocktails]);
    }

    /**
     * Show the form for creating a new resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function create()
    {
        return view('cocktail.create');
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $newPost = Cocktail::create([
            'name' => $request->name,
            'recipe' => $request->recipe
        ]);
        
        return redirect('cocktail/' . $newPost->id . '/show');
    }

    /**
     * Display the specified resource.
     *
     * @param  \App\Models\Cocktail  $cocktail
     * @return \Illuminate\Http\Response
     */
    public function show(Cocktail $cocktail)
    {
        return view('cocktail.show', compact('cocktail'));
    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param  \App\Models\Cocktail  $cocktail
     * @return \Illuminate\Http\Response
     */
    public function edit(Cocktail $cocktail)
    {
        return view('cocktail.edit', [
            'cocktail' => $cocktail,
        ]);
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \App\Models\Cocktail  $cocktail
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, Cocktail $cocktail)
    {
        $cocktail->update([
            'name' => $request->name,
            'recipe' => $request->recipe
        ]);
        
        return redirect('cocktail/' . $cocktail->id . '/edit')->with('success', 'true');
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  \App\Models\Cocktail  $cocktail
     * @return \Illuminate\Http\Response
     */
    public function delete(Cocktail $cocktail)
    {
        $cocktail->delete();
        return redirect('cocktails/')->with('success', 'true');
    }

    /**
     * Tests how a cocktail recipe will look
     *
     * @param  \App\Models\Cocktail  $cocktail
     * @return \Illuminate\Http\Response
     */
    public function test(Request $request)
    {
        $cocktail = unserialize(base64_decode($request->get('ser')));
        // return $cocktail;
        return view('cocktail.preview', compact('cocktail'));
    }
}

