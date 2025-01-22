document.addEventListener('DOMContentLoaded', function() {
    const eventDate = new Date("2026-01-10T00:00:00Z").getTime();

    const timer = setInterval(function() {
        const now = new Date().getTime();
        const distance = eventDate - now;

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        document.getElementById("countdown").innerHTML = `${days}d ${hours}h ${minutes}m ${seconds}s`;

        if (distance < 0) {
            clearInterval(timer);
            document.getElementById("countdown").innerHTML = "The event has started!";
        }
    }, 1000);
});