const pageSettingsElement = document.getElementById('page-settings');

if (pageSettingsElement) {
    let pageSettings = JSON.parse(pageSettingsElement.innerText);
    chrome.runtime.sendMessage(
        {
            message: "load-pageSettings",
            pageSettings: pageSettings,
        }
    );
    pageSettingsElement.remove();
}
