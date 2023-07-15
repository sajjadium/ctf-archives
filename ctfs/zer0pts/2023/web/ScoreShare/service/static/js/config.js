async function defaultConfig() {
    // Use cache if available
    if (window.config) return window.config;
    // Otherwise get config
    let promise = await fetch('/api/config');
    let config = await promise.json();
    return window.config = config;
}
