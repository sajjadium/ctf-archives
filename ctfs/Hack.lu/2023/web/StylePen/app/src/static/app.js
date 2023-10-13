function createCaptcha() {
    const sitekey = document.querySelector('meta[name="captcha-sitekey"]').getAttribute("content");
    const captchaContainer = document.createElement("div");
    captchaContainer.classList.add("frc-captcha");
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        captchaContainer.classList.add("dark"); // very important 👨‍💻
    }
    captchaContainer.dataset.attached = 1;
    document.getElementById("submission-form").appendChild(captchaContainer);
    new window.friendlyChallenge.WidgetInstance(captchaContainer, { sitekey: sitekey, solutionFieldName: "captcha-solution",  });
}

function sendSubmissionForm() {
    const form = document.getElementById("submission-form");
    if (!form.reportValidity()) return;
    const formData = new FormData(form);
    const solution = formData.get("captcha-solution");
    if (!solution || solution.startsWith(".")) {
        showAlert("Please complete the captcha before submitting", "error");
        form.reportValidity();
        return;
    }
    form.requestSubmit();
}

async function setupPage() {
    const formButton = document.getElementById("submission-button");
    formButton.addEventListener("click", sendSubmissionForm);

    createCaptcha();
    
    const codeOutput = document.getElementById('code-output');
    function updateCodeOutput(code) {
        codeOutput.innerHTML = DOMPurify.sanitize(code, { FORCE_BODY: true });
    }
    
    let debounceTimer;
    const codeArea = document.getElementById('submission-code');
    codeArea.oninput = () => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            location.hash = codeArea.value;
            updateCodeOutput(codeArea.value);
        }, 350);
    };

    const hash = window.location.hash;
    let code;
    if (hash) {
        code = decodeURIComponent(hash.substring(1));

    } else {
        code = await (await fetch("/static/example-code.html")).text();
    }
    codeArea.value = code;
    updateCodeOutput(code);
}

setupPage();
