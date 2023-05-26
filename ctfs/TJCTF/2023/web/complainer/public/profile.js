fetch('/api/verify', {
    method: 'GET',
    headers: {
        'Authorization': `Bearer ${localStorage.getItem('userId')}:${localStorage.getItem('sessionId')}`
    }
}).then(res => res.json()).then(res => {
    if (!res.ok)
        throw res.error;
}).catch(_ => {
    localStorage.removeItem('sessionId');
    localStorage.removeItem('userId');
    window.location = '/login';
});


fetch(`/api/profile`, {
    method: 'GET',
    headers: {
        'Authorization': `Bearer ${localStorage.getItem('userId')}:${localStorage.getItem('sessionId')}`
    }
}).then(res => res.json()).then(res => {
    console.log(res);
    for (const [idx, post] of res.user.posts.entries()) {
        const complaint = document.createElement('div');
        complaint.id = `complaint-${idx}`;
        complaint.className = 'complaint';

        complaint.innerHTML = [...post.body].map((c, i) => `<a href='/post/${post.id}' id='${idx}-${i}-${c}'>${c}</a>`).join('');

        document.getElementById('complaints').appendChild(complaint);

        const anchors = document.querySelectorAll(`#complaint-${idx} > a`);

        anchors.forEach((a, i) => {
            let size = 1;
            setInterval(() => {
                a.style.fontSize = `${(i + 1) / anchors.length * size}em`;
                size += 0.1;
            }, 100);
        });
    }
})
