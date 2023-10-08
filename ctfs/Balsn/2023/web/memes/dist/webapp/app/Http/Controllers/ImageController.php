<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class ImageController extends Controller
{

    public function index(Request $request)
    {
        if (!$request->input('image')) {
            $images = glob('memes/*.png');
            return view('image', ['images' => $images]);
        } else {
            $image = $request->input('image');
            return view('make-meme', ['image' => $image]);
        }
    }

    public function make(Request $request)
    {
        $texts = $request->input('texts');
        $sampleImage = $request->input('image');

        if (empty($texts)) {
            return redirect("/?image=$sampleImage");
        }

        $image = imagecreatefrompng($sampleImage);
        foreach ($texts as $text) {
            // hex color to rgb
            $text['color'] = ltrim($text['color'], '#');
            $text['color'] = array_map('hexdec', str_split($text['color'], 2));
            // add text
            $color = imagecolorallocate($image, $text['color'][0], $text['color'][1], $text['color'][2]);
            imagettftext($image, $text['size'], $text['angle'], $text['x'], $text['y'], $color, realpath("arial.ttf"), $text['text']);
        }
        
        $saveDir = str_replace(['memes/', '.png'], ['generated/', ''], $sampleImage);
        if (!file_exists($saveDir)) {
            mkdir($saveDir, 0777, true);
        }
        $imagePath = "$saveDir/" . bin2hex(random_bytes(8)) . '.png';
        imagepng($image, $imagePath);
        imagedestroy($image);

        // add created image into session
        $createdImages = $request->session()->get('createdImages', []);
        $createdImages[] = $imagePath;
        $request->session()->put('createdImages', $createdImages);

        return redirect("/list");
    }

    public function list(Request $request)
    {
        $createdImages = $request->session()->get('createdImages', []);
        // print html
        echo "<link rel='stylesheet' href='https://cdn.simplecss.org/simple.css'>";
        echo '<h1>Created Memes</h1>';
        foreach ($createdImages as $image) {
            echo "<img src='$image' alt='Created Image' style='width: 70%; height: auto;'>";
        }
        if (empty($createdImages)) {
            echo '<p>No memes created yet.</p>';
        }
    }

}
