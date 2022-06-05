(async () => {
    const src = chrome.runtime.getURL('assets/js/utils.js');
    const utils = await import(src);
    
    const setFont = async (font) => {

        if (!utils.FONTS.includes(font)) {

            // Special fonts, such as OpenDyslexic, are not supported by default.
            if (!font.includes('://')) {
                foo = await import(chrome.runtime.getURL(`assets/js/${font}.js`));
                foo.bar();
            }
            else {
                // Load external fonts.
                const customStyle = JSON.parse(document.getElementById('page-style').innerText);
                utils.setStyle(document.body, utils.merge({fontFamily: 'custom'}, customStyle));
                document.getElementById('page-style').remove();

                fetch(font, {
                    method: 'GET',
                    headers: {
                        'TOKEN': "REDACTED"
                    }
                }).then(response => response.text()).then(text => { 
                    const style = document.createElement("style");
                    style.textContent = text;
                    document.head.appendChild(style);
                });
            }
        }
        else if (font === 'Default') {

            // Reset font to original
            window.location.reload();
        }
        else {
            
            // Change font
            utils.mapElement(document.querySelector('body'), (element) => {
                element.style.fontFamily = font;
            });
        }
    }

    chrome.storage.local.get('font', async (result) => {
        await setFont(result.font);
        console.log('Changed font.');
    });
})();