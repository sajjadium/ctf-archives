// extra sanitization!

document.body.querySelectorAll("style").forEach(i => i.remove());
document.body.querySelectorAll("iframe").forEach(i => !i.src.startsWith("https://www.youtube.com") && i.remove());