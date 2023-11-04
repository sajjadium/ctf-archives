const ws = new WebSocket(`ws://${window.location.host}/admin/ws`);
ws.onopen = () => ws.send("increment");
