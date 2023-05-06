const hookForm = () => {
    function processForm(e) {
        if (e.preventDefault) e.preventDefault();
    
        const formElements = e.target.elements;

        const name = formElements['name'];
        const type = formElements['type'];

        const addData = {'widgetName': name.value, 'widgetData': JSON.stringify({'type': type.value})};

        fetch('/panel/add', {
            method: 'post',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(addData)
        });

        alert('Edit successfully sent! Check out your panels page again');

        return false;
    }

    const form = document.getElementById('edit-form');
    
    if (form.attachEvent) {
        form.attachEvent("submit", processForm);
    } else {
        form.addEventListener("submit", processForm);
    }
};

window.onload = () => {
    hookForm();
};