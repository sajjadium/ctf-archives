<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel='stylesheet' href='https://cdn.simplecss.org/simple.css'>
    <title>Meme Maker</title>
</head>

<body>
    <header>
        <h1>Meme Maker</h1>
        <p>Choose an image to make a meme</p>
        <a href="/list">List Your Memes</a>
    </header>


    <!-- list images -->
    @foreach ($images as $image)
    <div>
        Make a meme based on:<br>
        <a href="/?image={{ $image }}">
            <img src="{{ $image }}" style="width: 100%; height: auto;">
        </a>
    </div>
    @endforeach
</body>

</html>