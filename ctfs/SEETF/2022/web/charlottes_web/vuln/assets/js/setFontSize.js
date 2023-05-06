(async () => {
    const src = chrome.runtime.getURL('assets/js/utils.js');
    const utils = await import(src);

    function getFontSize(element) {
        const fontSize = window.getComputedStyle(element, null).getPropertyValue('font-size');
        return parseFloat(fontSize);
    }
    
    function getLineHeight(element) {
        let lineHeight = parseFloat(window.getComputedStyle(element, null).getPropertyValue('line-height'));
    
        if (isNaN(lineHeight)) {
            // Manually calculate line height
    
            const clone = element.cloneNode();
            clone.innerHTML = '<br>';
            element.appendChild(clone);
    
            const singleLineHeight = clone.offsetHeight;
            clone.innerHTML = '<br><br>';
    
            const doubleLineHeight = clone.offsetHeight;
    
            element.removeChild(clone);
            lineHeight = doubleLineHeight - singleLineHeight;
        }
    
        return lineHeight;
    }
    
    function setFontSize(percentage) {
        utils.mapElement(document.querySelector('body'), (element) => {
    
            // Change line height proportionally
            const lineHeight = getLineHeight(element);
            element.style.lineHeight = `${lineHeight * percentage / 100}px`;
    
            // Change font size
            const fontSize = getFontSize(element);
            element.style.fontSize = `${fontSize * percentage / 100}px`;
        });
    }
    
    chrome.storage.local.get('fontSize', (result) => {
        setFontSize(result.fontSize);
        console.log('Changed font size.');
    });    
})();