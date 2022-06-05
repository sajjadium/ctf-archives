(async () => {
    const src = chrome.runtime.getURL('assets/js/utils.js');
    const utils = await import(src);

    utils.mapElement(document.querySelector('body'), (element) => {
        // Remove previously-applied inline styles
        element.style.removeProperty('line-height');
        element.style.removeProperty('font-size');
    });
})();