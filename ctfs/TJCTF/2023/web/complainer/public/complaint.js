fetch('/api' + location.pathname).then(res => res.json()).then(res => {
    if (!res.ok)
        throw res.error;

    document.querySelector('.complaint').innerHTML = [...res.post.body].map((c, i) => `<span id='${i}-${c}'>${c}</span>`).join('');

    const spans = document.querySelectorAll('.complaint > span');

    spans.forEach((s, i) => {
        let size = 1;
        setInterval(() => {
            s.style.fontSize = `${(i + 1) / spans.length * size}em`;
            size += 0.1;
        }, 100);
    });
}).catch(err => {
    alert(err);
});
