<?php

namespace App\Http\Controllers;

use App\Models\Order;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

function get_balance($addr) {
    $res = Http::post("https://cloudflare-eth.com", [
        "jsonrpc" => "2.0",
        "method" => "eth_getBalance",
        "params" => [$addr, "latest"],
        "id" => 1
    ]);
    
    if ($res->ok()) {
        $data = $res->json();
        if (array_key_exists('error', $data)) {
            Log::error($res->body());
        } else {
            $b = $data['result'];
            return $b;
        }
    }
    
    return 0;
}

class OrderController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index(Request $request)
    {
        $orders = Order::find($request->session()->get('orders', []))->sortBy('created_at');

        return view('orders', [
            'orders' => $orders
        ]);
    }

    /**
     * Show the form for creating a new resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function create()
    {
        //
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        //
    }

    /**
     * Display the specified resource.
     *
     * @param  \App\Models\Order  $order
     * @return \Illuminate\Http\Response
     */
    public function show(Order $order)
    {
        $flag = '';
        
        $paid = $this->paid($order);
        if ($paid) {
            foreach(json_decode($order->items, true) as $i) {
                if ($i['name'] === 'flag') {
                    $flag = env('FLAG');
                }
            };
        }        
        
        return view('order', [
            'order' => $order,
            'flag' => $flag,
            'paid' => $paid,
        ]);
    }
    
    public function paid(Order $order) {
        $b = get_balance($order->wallet);
        $t = gmp_mul((int)($order->total * 100), (int)1e16);
        
        return gmp_cmp($b, $t) >= 0;
    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param  \App\Models\Order  $order
     * @return \Illuminate\Http\Response
     */
    public function edit(Order $order)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \App\Models\Order  $order
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, Order $order)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  \App\Models\Order  $order
     * @return \Illuminate\Http\Response
     */
    public function destroy(Order $order)
    {
        //
    }
}
