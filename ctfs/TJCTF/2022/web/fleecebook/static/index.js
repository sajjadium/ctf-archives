const f = document.getElementById('fleece');
document.addEventListener('mousemove', e => {
    f.style.top = `${e.clientY}px`;
    f.style.left = `${e.clientX}px`;
});
