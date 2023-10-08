<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel='stylesheet' href='https://cdn.simplecss.org/simple.css'>
    <title>Create Meme</title>
</head>

<body>
    <h1>Create Meme with Text</h1>
    <div><canvas id="canvas" style="width: -webkit-fill-available; width: -moz-available;"></canvas></div>

    <form action="/make" method="POST">
        @csrf <!-- Laravel CSRF token -->

        <input type="hidden" name="image" value="{{$image}}">
        <div id="textFields"></div>
        <button type="button" id="addTextButton">Add Text</button>
        <button type="button" id="editColorButton">Edit Color</button>
        <button type="button" id="deleteTextButton">Delete Text</button>
        <hr>
        <input type="submit" value="Create Image">
    </form>
    <input type="color" id="colorPicker" style="visibility: hidden">

    <script src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.3.1/fabric.min.js"></script>

    <script>
        const texts = {}

        const templateImage = '{{$image}}';
        const canvas = new fabric.Canvas('canvas', {
            selection: false,
            keyboardEventsEnabled: true,
        });
        fabric.Image.fromURL(templateImage, (img) => {
            // change canvas size to image size, but keep aspect ratio
            canvas.setWidth(img.width);
            canvas.setHeight(img.height);
            // add image to canvas
            canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas));
        });

        const textFields = document.getElementById('textFields');
        const addTextButton = document.getElementById('addTextButton');
        addTextButton.onclick = () => {
            const text = new fabric.IText('Text', {
                left: 100 + Object.keys(texts).length * 10,
                top: 100 + Object.keys(texts).length * 10,
                fontSize: 32,
                fontFamily: 'arial',
                padding: 0,
                fill: '#000000'
            });
            text.setControlsVisibility({
                mt: false,
                mb: false,
                ml: false,
                mr: false
            });
            const id = `text-${Object.keys(texts).length}`;
            text.id = id;
            texts[id] = text;
            canvas.add(text);
        }

        const editColorButton = document.getElementById('editColorButton');
        editColorButton.onclick = () => {
            const activeObject = canvas.getActiveObject();
            if (activeObject) {
                // create color picker
                const colorPicker = document.getElementById('colorPicker');
                colorPicker.value = activeObject.fill;

                colorPicker.click();
                colorPicker.oninput = () => {
                    activeObject.set('fill', colorPicker.value);
                    canvas.renderAll();
                    colorPicker.style.display = 'none';
                }
            }
        }

        const deleteTextButton = document.getElementById('deleteTextButton');
        deleteTextButton.onclick = () => {
            const activeObject = canvas.getActiveObject();
            if (activeObject) {
                canvas.remove(activeObject);
                delete texts[activeObject.id];
            }
        }

        const form = document.querySelector('form');
        form.addEventListener('submit', (event) => {
            event.preventDefault();
            const textFields = Object.values(texts).map((text, i) => `
                <input type="hidden" name="texts[${i}][text]" value="${text.text}">
                <input type="hidden" name="texts[${i}][x]" value="${text.aCoords.bl.x}">
                <input type="hidden" name="texts[${i}][y]" value="${text.aCoords.bl.y}">
                <input type="hidden" name="texts[${i}][size]" value="${text.fontSize * text.scaleX}">
                <input type="hidden" name="texts[${i}][color]" value="${text.fill}">
                <input type="hidden" name="texts[${i}][angle]" value="${360 - text.angle}">
            `).join('');
            form.insertAdjacentHTML('beforeend', textFields);
            form.submit();
        });
    </script>
</body>

</html>