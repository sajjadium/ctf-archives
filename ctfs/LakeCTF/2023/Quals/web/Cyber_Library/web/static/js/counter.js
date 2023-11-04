const enableBtn = document.getElementById('enable-live-statistics');
const counter = document.getElementById('counter');
counter.innerText = Math.ceil(Math.random() * 1337);

enableBtn.addEventListener('click', (e) => {
    enableBtn.style.display = 'none';
    e.preventDefault();
    const ws = new WebSocket(`ws://${window.location.host}/ws`);
    ws.onmessage = (event) => {
        counter.innerText = event.data;
    };
    // Save resources 🍃♻️💚
    setTimeout(() => {
        ws.close();
        enableBtn.style.display = 'block';
    }, 60*1000);
});
