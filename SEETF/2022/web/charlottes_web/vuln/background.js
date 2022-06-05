import * as utils from './assets/js/utils.js';

const getCurrentTab = async () => {
    let queryOptions = { active: true, currentWindow: true };
    let [tab] = await chrome.tabs.query(queryOptions);
    return tab;
}

const changeFontSize = () => {
    getCurrentTab().then((tab) => {
        chrome.scripting.executeScript({
            target: { tabId: tab.id },
            files: [
                "./assets/js/resetFontSize.js",
                "./assets/js/setFontSize.js",
            ],
        });
    });
};

const changeFont = () => {
    getCurrentTab().then((tab) => {
        chrome.scripting.executeScript({
            target: { tabId: tab.id },
            files: [
                "./assets/js/setFont.js",
            ],
        });
    });
}

const applyPageSettings = (newSettings) => {
    chrome.storage.local.get(null, (result) => {

        let settings = utils.merge(result, newSettings);

        // Validate fonts
        let valid = false;
        for (let i = 0; i <= utils.FONTS.length; i++) {
            if (settings.font === utils.FONTS[i]) {
                valid = true;
                break;
            }
        }

        if (!valid) { 
            console.log("Validation failed.")
            return; 
        }

        chrome.storage.local.set(settings, () => {
            if (settings.font)
                changeFont();
            if (settings.fontSize)
                changeFontSize();
            console.log('Applied settings.');
        });
    });
}

chrome.runtime.onMessage.addListener(
    (request, sender, sendResponse) => {
        if (request.message === "load-fontSize") {
            changeFontSize();
            sendResponse({ success: true });
        }
        else if (request.message === "load-fontChange") {
            changeFont();
            sendResponse({ success: true });
        }
        else if (request.message === "load-pageSettings") {
            applyPageSettings(request.pageSettings);
            sendResponse({ success: true });
        }
    }
);