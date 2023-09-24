document.addEventListener('DOMContentLoaded', function() {
    const loadingContainer = document.querySelector('.loading-container');
    setTimeout(() => {
        loadingContainer.style.display = 'none';
    }, 6000);
});
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/scripts/service-worker.js')
      .then(registration => {
        console.log('Service Worker registered:', registration);
      })
      .catch(error => {
        console.error('Error registering Service Worker:', error);
      });
  }