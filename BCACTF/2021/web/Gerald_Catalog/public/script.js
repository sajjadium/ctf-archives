window.addEventListener("load", _ => {
    document.querySelectorAll(".mdc-button").forEach(button => {
        mdc.ripple.MDCRipple.attachTo(button);
    });
    mdc.topAppBar.MDCTopAppBar.attachTo(document.querySelector(".mdc-top-app-bar"));
    document.querySelectorAll(".mdc-text-field").forEach(field => {
        mdc.textField.MDCTextField.attachTo(field);
    });
    document.querySelectorAll(".mdc-switch").forEach(s => {
        mdc.switchControl.MDCSwitch.attachTo(s);
    });
});