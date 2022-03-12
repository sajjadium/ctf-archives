
var canvas;
var ctx;

window.onload = () => {
    canvas = document.getElementById("display-canvas");
    ctx = canvas.getContext("2d");

    Module.onRuntimeInitialized = () => {
        imgData = document.getElementById("posted-data").value;
        if(imgData !== "") {
            draw_u8a(Uint8Array.from(atob(imgData), c => c.charCodeAt(0)));
        }
    }
}

function draw(x, y, r, g, b, a) {
    ctx.fillStyle = "rgba(" + r + ", " + g + ", " + b + ", " + a + ")";
    ctx.fillRect(x, y, 1, 1);
}

function draw_buf(buf_offset, width, height) {
    let buf = new Uint8Array(Module.HEAPU8.buffer, buf_offset, width * height * 4);
    for (let x = 0; x < width; x++) {
        for (let y = 0; y < height; y++) {
            let i = (y * width + x) * 4;
            draw(x, y, buf[i], buf[i + 1], buf[i + 2], buf[i + 3]);
        }
    }
}

function draw_u8a(img) {
    draw_img = Module.cwrap("draw_img", null, ['number', 'number']);
        
    let buf_offset = Module._malloc(img.length);
    Module.HEAPU8.set(img, buf_offset);

    draw_img(buf_offset, img.length);
}

async function handle_draw_click() {
    let fileNode = document.getElementById("file_picker");
    let file = fileNode.files[0];
    let reader = new FileReader();
    reader.onload = function(e) {
        let data = btoa(e.target.result);
        
        document.getElementById("image-data").value = data;
        document.getElementById("hidden-form").submit();
    }
    reader.readAsBinaryString(file);
}