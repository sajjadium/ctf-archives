import { createCanvas, loadImage, PNGStream } from "canvas";

const geraldImage = loadImage("gerald.PNG");

export async function generateGerald(caption: string): Promise<PNGStream> {
    const gerald = await geraldImage;
    const canvas = createCanvas(gerald.width, gerald.height);
    const ctx = canvas.getContext("2d");
    ctx.drawImage(gerald, 0, 0);
    ctx.font = "24px 'Comic Sans MS'";
    ctx.fillStyle = "black";
    ctx.fillText(caption, 100, 150, gerald.width - 300);
    return canvas.createPNGStream();
}