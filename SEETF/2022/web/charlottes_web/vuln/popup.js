const fontSizeSlider = document.querySelector('#fontSizeSlider');
const fontSizeLabel = document.querySelector("label[for='fontSizeSlider']");
const fontChangeOption = document.querySelector('#fontChange');

const changeSliderLabelValue = (element, slider) => {
    element.innerHTML = slider.value;
};


const setFontSize = (value) => {
    chrome.runtime.sendMessage(
        {
            message: "load-fontSize",
            fontSize: value,
        }
    );
};


const setFont = (value) => {
    chrome.runtime.sendMessage(
        {
            message: "load-fontChange",
            font: value,
        }
    );
};


fontSizeSlider.addEventListener('change', (e) => {
    chrome.storage.local.set(
        {
            fontSize: parseInt(e.target.value, 10),
        },
        () => {
            setFontSize(parseInt(e.target.value, 10));
            changeSliderLabelValue(fontSizeLabel, fontSizeSlider);
        }
    );
});


fontChangeOption.addEventListener('change', (e) => {
    chrome.storage.local.set(
        {
            font: e.target.value,
        },
        () => {
            setFont(e.target.value);
        }
    )
});

