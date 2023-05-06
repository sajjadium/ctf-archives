export const bar = async () => {
    const src = chrome.runtime.getURL('assets/js/utils.js');
    const utils = await import(src);

    const style = document.createElement("style");
    style.textContent = `
    @font-face {
        font-family: 'opendyslexic';
        src: url(${chrome.runtime.getURL('assets/fonts/opendyslexic/OpenDyslexic-Regular.otf')});
        font-style: normal;
        font-weight: normal;
    }
    @font-face {
        font-family: 'opendyslexic';
        src: url(${chrome.runtime.getURL('assets/fonts/opendyslexic/OpenDyslexic-Italic.otf')});
        font-style: italic;
        font-weight: normal;
    }
    @font-face {
        font-family: 'opendyslexic';
        src: url(${chrome.runtime.getURL('assets/fonts/opendyslexic/OpenDyslexic-Bold.otf')});
        font-weight: bold;
        font-style: normal;
    }
    @font-face {
        font-family: 'opendyslexic';
        src: url(${chrome.runtime.getURL('assets/fonts/opendyslexic/OpenDyslexic-BoldItalic.otf')});
        font-weight: bold;
        font-style: italic;
    }
    @font-face {
        font-family: 'opendyslexicmono';
        src: url(${chrome.runtime.getURL('assets/fonts/opendyslexic/OpenDyslexicMono-Regular.otf')});
        font-weight: normal;
        font-style: normal;
    }
    `;
    document.head.appendChild(style);
    
    utils.mapElement(document.querySelector('body'), (element) => {
        element.style.fontFamily = 'opendyslexic';
    });
};