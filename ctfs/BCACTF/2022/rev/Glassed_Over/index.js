const jimp = require('jimp');

async function main() {
    const image = await jimp.read('flag.png');
    const width = image.bitmap.width;
    const height = image.bitmap.height;
    
    image.scan(0, 0, width, height, (x, y, idx)=>{
        // var red = image.bitmap.data[idx];
        // var green = image.bitmap.data[idx + 1];
        // var blue = image.bitmap.data[idx + 2];
        // var alpha = image.bitmap.data[idx + 3];
        
        image.bitmap.data[idx+3] = Math.random() * 12;
        image.bitmap.data[idx+2] -= 129;
        image.bitmap.data[idx+1] -= 68;

        if (x == image.bitmap.width - 1 && y == image.bitmap.height - 1) {
            image.write("modifiedflag.png");
        }
    });

}
main();