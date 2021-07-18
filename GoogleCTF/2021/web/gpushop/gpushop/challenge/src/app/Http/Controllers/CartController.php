<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Product;
use App\Models\Order;

class CartController extends Controller
{
    public function index(Request $request)
    {
        if (\Cart::isEmpty()) {
            return view('cart', ['items' => \Cart::getContent()]);
        }
        
        $subtotal = \Cart::getSubTotal();
        $total = \Cart::getTotal();
        $condition = \Cart::getCondition('Scalper Tax');
        $tax = $condition->getCalculatedValue($subtotal);
        
        return view('cart', [
            'items' => \Cart::getContent(),
            'subtotal' => $subtotal,
            'total' => $total,
            'tax' => $tax
        ]);
    }
    
    public function add(Request $request, $id)
    {
        $p = Product::findOrFail($id);
        
        $condition = new \Darryldecode\Cart\CartCondition(array(
            'name' => 'Scalper Tax',
            'type' => 'tax',
            'target' => 'total',
            'value' => '15%',
            'attributes' => array(
                'description' => 'Scalper tax',
            )
        ));
        
        \Cart::condition($condition);        
        
        \Cart::add($p->id, $p->name, $p->price, 1, array());
        
        return redirect()->action([CartController::class, 'index']);
    }
    
    public function clear()
    {
        \Cart::clear();
        
        return redirect()->action([CartController::class, 'index']);
    }
    
    public function checkout(Request $request)
    {
        if (!\Cart::isEmpty()) {
            $order = new Order;
            $order->id = bin2hex(random_bytes(20));
            $order->address = $request->input('address');
            $order->wallet = $this->format_addr($request->header('X-Wallet'));
            $order->total = \Cart::getTotal();
            $order->items = \Cart::getContent()->toJson();
            $order->save();
            
            $request->session()->push('orders', $order->id);
            
            \Cart::clear();
        }
        
        return redirect()->action([OrderController::class, 'index']);
    }
    
    function format_addr($addr) {
        return '0x'.str_pad($addr, 40, '0', STR_PAD_LEFT);
    }        
}
